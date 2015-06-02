"""
BaseOAuth is inspired from Darren Kempiners YahooAPI https://github.com/dkempiners/python-yahooapi/blob/master/yahooapi.py
"""
from __future__ import absolute_import

try:
    input = raw_input
except NameError:
    pass

import pdb
import json
import time
import logging
import webbrowser

from rauth import OAuth1Service, OAuth2Service
from rauth.utils import parse_utf8_qsl

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s %(levelname)s] [%(name)s.%(module)s.%(funcName)s] %(message)s")
logging.getLogger('yahoo-oauth')


def json_write_data(json_data, filename):
    """Write json data into a file
    """
    with open(filename, 'w') as fp:
        json.dump(json_data, fp, indent=4, sort_keys=True, ensure_ascii=False)
        return True
    return False

def json_get_data(filename):
    """Get data from json file
    """
    with open(filename) as fp:
        json_data = json.load(fp)
        return json_data

    return False

services = {
    'oauth1' : dict(
        SERVICE = OAuth1Service,
        REQUEST_TOKEN_URL = "https://api.login.yahoo.com/oauth/v2/get_request_token",
        ACCESS_TOKEN_URL = "https://api.login.yahoo.com/oauth/v2/get_token",
        AUTHORIZE_TOKEN_URL = "https://api.login.yahoo.com/oauth/v2/request_auth"
    ),
    'oauth2' : dict(
        SERVICE = OAuth2Service,
        AUTHORIZE_TOKEN_URL = "https://api.login.yahoo.com/oauth2/request_auth",
        ACCESS_TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
    )
}
CALLBACK_URI = 'oob'


class BaseOAuth(object):
    """
    """
    def __init__(self, oauth_version, consumer_key, consumer_secret, **kwargs):
        """
        consumer_key : client key
        consumer_secret : client secret
        access_token : access token
        access_token_secret : access token secret
        from_file : file containing the credentials
        """
        self.oauth_version = oauth_version
        
        if kwargs.get('from_file'):
            logging.debug("Checking ")
            self.from_file = kwargs.get('from_file')
            json_data = json_get_data(self.from_file)
            vars(self).update(json_data)
        else:
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret

        vars(self).update(kwargs)

        self.oauth_version = oauth_version
        self.callback_uri = vars(self).get('callback_uri',CALLBACK_URI)

        # Init OAuth
        if self.oauth_version == 'oauth1':
            service_params = {
                'consumer_key': self.consumer_key,
                'consumer_secret' : self.consumer_secret,
                'request_token_url': services[self.oauth_version]['REQUEST_TOKEN_URL']
            }
        else:
            service_params = {
                'client_id': self.consumer_key,
                'client_secret': self.consumer_secret
            }

        service_params.update({
            'name' : 'yahoo',
            'access_token_url' : services[self.oauth_version]['ACCESS_TOKEN_URL'],
            'authorize_url' : services[self.oauth_version]['AUTHORIZE_TOKEN_URL'],
            'base_url': vars(self).get('base_url',None)
        })
        self.oauth = services[oauth_version]['SERVICE'](**service_params)
        

        if vars(self).get('access_token') and vars(self).get('access_token_secret') and vars(self).get('session_handle'):
            if not self.token_is_valid():
                self.session = self.refresh_token() 
        else:
            if self.oauth_version == 'oauth1':
                self.oauth1_handler()
            else:
                self.oauth2_handler()
            
        self.session = self.oauth.get_session((self.access_token, self.access_token_secret))

        json_data.update({
            'access_token' : self.access_token,
            'access_token_secret' : self.access_token_secret,
            'session_handle' : self.session_handle,
            'token_time' : self.token_time
        })

        json_write_data(json_data, self.from_file)

    def oauth1_handler(self,):
        """get request token, redirect user and get access tokens
        """
        request_token, request_token_secret = self.oauth.get_request_token(params={'oauth_callback': self.callback_uri})
        logging.debug("REQUEST_TOKEN = {0}\n REQUEST_TOKEN_SECRET = {1}\n".format(request_token, request_token_secret))

        authorize_url = self.oauth.get_authorize_url(request_token)
        logging.debug(authorize_url)
        webbrowser.open(authorize_url)
        verifier = input("Enter verifier : ")
        logging.debug("VERIFIER = {0}".format(verifier))

        self.token_time = time.time()
        raw_access = self.oauth.get_raw_access_token(request_token, request_token_secret, params={"oauth_verifier": verifier})
        parsed_acess = parse_utf8_qsl(raw_access.content)

        self.access_token = parsed_acess['oauth_token']
        self.access_token_secret = parsed_acess['oauth_token_secret']
        self.session_handle = parsed_acess['oauth_session_handle']

    def oauth2_handler(self,):
        """
        """
        url = self.oauth.get_authorize_url(client_secret=self.consumer_secret, redirect_uri=self.callback_uri, response_type='code')
        logging.debug("AUTHORISATION URL : {0}".format(url))
        webbrowser.open(url)
        verifier = input("Enter verifier : ")
        logging.debug("VERIFIER = {0}".format(verifier))
        raw_access = self.oauth.get_raw_access_token(params={"code": verifier})
        pdb.set_trace() 
        self.oauth.get_auth_session(data={'code':verifier, 'redirect_uri': self.callback_uri})

    def refresh_token(self,):
        """Refresh access token
        """
        logging.debug("REFRESHING TOKEN")
        self.token_time = time.time()
        self.access_token, self.access_token_secret = self.oauth.get_access_token(self.access_token, self.access_token_secret, params={"oauth_session_handle": self.session_handle})

        session = self.oauth.get_session((self.access_token, self.access_token_secret))

        return session

    def token_is_valid(self,):
        """Check the validity of the token :3600s
        """
        elapsed_time = time.time() - self.token_time
        logging.debug("ELAPSED TIME : {0}".format(elapsed_time))
        if elapsed_time > 3540: # 1 minute before it expires
            logging.debug("TOKEN HAS EXPIRED")
            return False

        logging.debug("TOKEN IS STILL VALID")
        return True


class OAuth1(BaseOAuth):
    """Class handling OAuth v1
    """

    def __init__(self, consumer_key, consumer_secret, **kwargs):
        
        super(OAuth1, self).__init__('oauth1', consumer_key, consumer_secret, **kwargs)


class OAuth2(BaseOAuth):
    """Calss handling OAuth v2
    """

    def __init__(self, consumer_key, consumer_secret, **kwargs):
       
        super(OAuth2, self).__init__('oauth2', consumer_key, consumer_secret, **kwargs)

     
