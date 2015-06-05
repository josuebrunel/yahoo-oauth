"""Base OAuth Class
"""
from __future__ import absolute_import

import json
import logging
import webbrowser

import base64

from rauth import OAuth1Service, OAuth2Service
from rauth.utils import parse_utf8_qsl

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s %(levelname)s] [%(name)s.%(module)s.%(funcName)s] %(message)s")
logging.getLogger('yahoo-oauth')

services = {
    'oauth1':{ 
        SERVICE : OAuth1Service,
        REQUEST_TOKEN_URL : "https://api.login.yahoo.com/oauth/v2/get_request_token",
        ACCESS_TOKEN_URL : "https://api.login.yahoo.com/oauth/v2/get_token",
        AUTHORIZE_TOKEN_URL : "https://api.login.yahoo.com/oauth/v2/request_auth"
        },
    'oauth2': {
        SERVICE : OAuth2Service,
        AUTHORIZE_TOKEN_URL : "https://api.login.yahoo.com/oauth2/request_auth",
        ACCESS_TOKEN_URL : "https://api.login.yahoo.com/oauth2/get_token"
    }
}

CALLBACK_URI = 'oob'


class OAuthBase(object):
    """OAuth Class
    """

    def __init__(self, oauth_version, consumer_key, consumer_secret, **kwargs):
        """Initialize an oauth class
        consumer_key : client key
        consumer_secret : client secret
        access_token: access token
        base_url : base url
        access_token_secret: access_token_secret
        callback_uri : callback uri
        from_file: file's path containing credentials
        """

        self.oauth_version = oauth_version

        if kwargs.get('from_file'):
            self.from_file = kwargs.get('from_file')
            json_data = self.json_get_data(self.from_file)
            vars(self).update(json_data)
        else:
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret

        vars(self).update(kwargs)

        self.callback_uri = vars(self).get('callback_uri',CALLBACK_URI)

        # Initializing service
        if self.oauth_version == 'oauth1':
            service_params = {
                'consumer_key': self.consumer_key,
                'consumer_secret': self.consumer_secret,
                'request_token_url': services[self.oauth_version]['REQUEST_TOKEN_URL']
            }
        else:
            service_params = {
                'client_id': self.consumer_key,
                'consumer_secret': self.consumer_secret,
            }

        service_params.update({
            'name': 'yahoo',
            'access_token_url': services[self.oauth_version]['ACCESS_TOKEN_URL'],
            'authorize_url': services[self.oauth_version]['AUTHORIZE_TOKEN_URL'],
            'base_url': vars(self).get('base_url',None)
        })

        self.service = services[self.oauth_version]['SERVICE'](**service_params)

    def json_get_data(self, filename):
        """Get data from json file
        """
        with open(filename) as fp:
            json_data = json.load(fp)
            return json_data
        return False

    def json_write_data(self, data, filename):
        """Write data into json file 
        """
        with open(filename, 'w') as fp:
            json.dump(data, fp, indent=4, sort_keys=True, ensure_ascii=False)
            return True
        return False

    def is_token_valid(self,):
        """Check if token is still valid
        """
        elapsed_time = time.time() - self.token_time
        logging.debug("elapsed time : {0}".format(elapsed_time))

        if elapsed_time > 3540: # 1 min before expiration
            logging.debug("token has expired")
            return False

        logging.debug("token is valid")
        return True


