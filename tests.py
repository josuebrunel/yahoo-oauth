from __future__ import absolute_import

import os, pdb, logging, unittest

import myql
from myql.utils import pretty_json

from yahoo_oauth.yahoo_oauth import json_write_data, json_get_data
from yahoo_oauth import OAuth1, OAuth2

logging.basicConfig(level=logging.DEBUG,format="[%(asctime)s %(levelname)s] [%(name)s.%(module)s.%(funcName)s] %(message)s \n")
logging.getLogger('yahoo-oauth')

logging.getLogger('yahoo-oauth').setLevel(logging.WARNING)

class TestYahooOAuth(unittest.TestCase):
    """Class to tests Yahoo OAuth module
    """

    def setUp(self,):
        self.d = {'ck':'consumer_key','cs':'consumer_secret'} 

    def tearDown(self):
        pass

    def test_1_json_write_data(self,):
        json_write_data(self.d, 'test.json')
        self.assertEquals(os.path.exists('test.json'),True)

    def test_2_json_get_data(self,):
        json_data = json_get_data('test.json')
        self.assertEquals(self.d,json_data)

    def test_oauth1(self,):
        oauth = OAuth1(None, None, from_file='oauth1.json')
        yql = myql.MYQL(oauth=oauth)
        response = yql.getGUID('josue_brunel')
        logging.debug(pretty_json(response.content)) 
        self.assertEqual(response.status_code,200)

    def test_oauth2(self,):
        oauth = OAuth2(None, None, from_file='oauth2.json')
        response = oauth.session.get('https://social.yahooapis.com/v1/me/guid?format=json')
        logging.debug(pretty_json(response.content)) 
        self.assertEqual(response.status_code,200)
