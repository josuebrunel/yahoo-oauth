"""
BaseOAuth is inspired from Darren Kempiners YahooAPI https://github.com/dkempiners/python-yahooapi/blob/master/yahooapi.py
"""
from __future__ import absolute_import

try:
    input = raw_input
except NameError:
    pass

import json
import time
import logging
import webbrowser

import base64

from rauth.utils import parse_utf8_qsl

from yahoo_oauth.utils import services, CALLBACK_URI, STORE_FILE_FLAG
from yahoo_oauth.utils import get_data, write_data


logger = logging.getLogger('yahoo_oauth')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s %(levelname)s] [%(name)s.%(module)s.%(funcName)s] %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


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
        base_url : Base url
        """
        self.oauth_version = oauth_version
        data = {}
        if kwargs.get('from_file'):
            logger.debug("Checking ")
            self.from_file = kwargs.get('from_file')
            data = get_data(self.from_file)
            vars(self).update(data)
        else:
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret

        vars(self).update(kwargs)

        self.oauth_version = oauth_version
        self.callback_uri = vars(self).get('callback_uri', CALLBACK_URI)
        self.store_file = vars(self).get('store_file', STORE_FILE_FLAG)

        if 'browser_callback' in kwargs.keys():
            self.browser_callback = kwargs.get('browser_callback')
        else:
            self.browser_callback = True

        # Init OAuth
        service_params = {
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret
        }

        service_params.update({
            'name': 'yahoo',
            'access_token_url': services[self.oauth_version]['ACCESS_TOKEN_URL'],
            'authorize_url': services[self.oauth_version]['AUTHORIZE_TOKEN_URL'],
            'base_url': vars(self).get('base_url', None)
        })

        # Defining oauth service
        self.oauth = services[oauth_version]['SERVICE'](**service_params)

        if vars(self).get('access_token') and vars(self).get('access_token_secret') and vars(self).get('session_handle'):
            if not self.token_is_valid():
                data.update(self.refresh_access_token())
        elif vars(self).get('access_token') and vars(self).get('token_type') and vars(self).get('refresh_token'):
            if not self.token_is_valid():
                data.update(self.refresh_access_token())
        else:
            data.update(self.handler())

        # Getting session
        self.session = self.oauth.get_session(token=self.access_token)

        if self.store_file:
            write_data(data, vars(self).get('from_file', 'secrets.json'))

    def handler(self,):

        authorize_url = self.oauth.get_authorize_url(redirect_uri=self.callback_uri, response_type='code')

        logger.debug("AUTHORIZATION URL : {0}".format(authorize_url))
        if self.browser_callback:
            # Open authorize_url
            webbrowser.open(authorize_url)
            self.verifier = input("Enter verifier : ")
        else:
            self.verifier = input("AUTHORIZATION URL : {0}\nEnter verifier : ".format(authorize_url))

        self.token_time = time.time()

        credentials = {'token_time': self.token_time}

        # Building headers
        headers = self.generate_oauth2_headers()
        # Getting access token
        raw_access = self.oauth.get_raw_access_token(data={"code": self.verifier, 'redirect_uri': self.callback_uri, 'grant_type': 'authorization_code'},
                                                     headers=headers)
        #  parsed_access = parse_utf8_qsl(raw_access.content.decode('utf-8'))
        credentials.update(self.oauth2_access_parser(raw_access))

        return credentials

    def generate_oauth2_headers(self):
        """Generates header for oauth2
        """
        encoded_credentials = base64.b64encode(('{0}:{1}'.format(self.consumer_key, self.consumer_secret)).encode('utf-8'))
        headers = {
            'Authorization': 'Basic {0}'.format(encoded_credentials.decode('utf-8')),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        return headers

    def oauth2_access_parser(self, raw_access):
        """Parse oauth2 access
        """
        parsed_access = json.loads(raw_access.content.decode('utf-8'))
        self.access_token = parsed_access['access_token']
        self.token_type = parsed_access['token_type']
        self.refresh_token = parsed_access['refresh_token']
        self.guid = parsed_access.get('xoauth_yahoo_guid', None)

        credentials = {
            'access_token': self.access_token,
            'token_type': self.token_type,
            'refresh_token': self.refresh_token,
            'guid': self.guid
        }
        return credentials

    def refresh_access_token(self,):
        """Refresh access token
        """
        logger.debug("REFRESHING TOKEN")
        self.token_time = time.time()
        credentials = {
            'token_time': self.token_time
        }

        headers = self.generate_oauth2_headers()

        raw_access = self.oauth.get_raw_access_token(
            data={"refresh_token": self.refresh_token, 'redirect_uri': self.callback_uri, 'grant_type': 'refresh_token'}, headers=headers)
        credentials.update(self.oauth2_access_parser(raw_access))

        return credentials

    def token_is_valid(self,):
        """Check the validity of the token :3600s
        """
        elapsed_time = time.time() - self.token_time
        logger.debug("ELAPSED TIME : {0}".format(elapsed_time))
        if elapsed_time > 3540:  # 1 minute before it expires
            logger.debug("TOKEN HAS EXPIRED")
            return False

        logger.debug("TOKEN IS STILL VALID")
        return True


class OAuth2(BaseOAuth):
    """Calss handling OAuth v2
    """

    def __init__(self, consumer_key, consumer_secret, **kwargs):
        super(OAuth2, self).__init__('oauth2', consumer_key, consumer_secret, **kwargs)
