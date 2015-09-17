from __future__ import absolute_import, unicode_literals

import json
import yaml
from rauth import OAuth1Service, OAuth2Service

services = {
    'oauth1': dict(
        SERVICE = OAuth1Service,
        REQUEST_TOKEN_URL = "https://api.login.yahoo.com/oauth/v2/get_request_token",
        ACCESS_TOKEN_URL = "https://api.login.yahoo.com/oauth/v2/get_token",
        AUTHORIZE_TOKEN_URL = "https://api.login.yahoo.com/oauth/v2/request_auth"
    ),
    'oauth2': dict(
        SERVICE = OAuth2Service,
        AUTHORIZE_TOKEN_URL = "https://api.login.yahoo.com/oauth2/request_auth",
        ACCESS_TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
    )
}

CALLBACK_URI = 'oob'

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

def yaml_get_data(filename):
    """Get data from .yml file
    """
    with open(filename, 'rb') as fd:
        yaml_data = yaml.load(fd)
        return yaml_data
    return False

def yaml_write_data(yaml_data, filename):
    """Write data into a .yml file
    """
    with open(filename, 'w') as fd:
        yaml.dump(yaml_data, fd, default_flow_style=False)
        return True

    return False

