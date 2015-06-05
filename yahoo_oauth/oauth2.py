"""Yahoo OAuth2 Module
"""
from __future__ import absolute_import

from yahoo_oauth import OAuthBase


class OAuth2(OAuthBase):

    def __init__(self, consumer_key, consumer_secret, **kwargs):

        super(OAuth2, self).__init__('oauth2', consumer_key, consumer_secret, **kwargs)
