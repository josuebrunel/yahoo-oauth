"""Yahoo OAuth1 Module
"""
from __future__ import absolute_import

from yahoo_oauth import OAuthBase


class OAuth1(OAuthBase):

    def __init__(self, consumer_key, consumer_secret, **kwargs):

        super(OAuth1, self).__init__('oauth1', consumer_key, consumer_secret, **kwargs)
