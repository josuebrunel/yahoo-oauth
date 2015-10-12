from __future__ import absolute_import

import os, pdb, logging, unittest

import myql
from myql.utils import pretty_json

from yahoo_oauth.utils import write_data, get_data
from yahoo_oauth.utils import json_write_data, json_get_data
from yahoo_oauth.utils import yaml_write_data, yaml_get_data
from yahoo_oauth import OAuth1, OAuth2

logging.basicConfig(level=logging.DEBUG,format="[%(asctime)s %(levelname)s] [%(name)s.%(module)s.%(funcName)s] %(message)s \n")
oauth_logger = logging.getLogger('yahoo_oauth')

oauth_logger.disabled = False


class TestYahooOAuth(unittest.TestCase):
    """Class to tests Yahoo OAuth module
    """
    def test_oauth1(self,):
        oauth = OAuth1(None, None, from_file='oauth1.json')
        yql = myql.MYQL(oauth=oauth)
        response = yql.get_guid('josue_brunel')
        logging.debug(pretty_json(response.content)) 
        self.assertEqual(response.status_code,200)

    def test_oauth2(self,):
        oauth = OAuth2(None, None, from_file='oauth2.yaml')
        response = oauth.session.get('https://social.yahooapis.com/v1/me/guid?format=json')
        logging.debug(pretty_json(response.content)) 
        self.assertEqual(response.status_code,200)


class TestJSON(unittest.TestCase):

    def setUp(self,):
        self.d = {'ck':'consumer_key','cs':'consumer_secret'} 

    def tearDown(self):
        pass

    def test_1_json_write_data(self,):
        write_data(self.d, 'data.json')
        self.assertEquals(os.path.exists('data.json'), True)

    def test_2_json_get_data(self,):
        json_data = get_data('data.json')
        self.assertEquals(self.d,json_data)


class TestYAML(unittest.TestCase):

    def setUp(self,):
        self.d = {'ck': 'consumer_key', 'cs': 'consumer_key'}

    def test_1_yaml_write_data(self,):
        yaml_write_data(self.d, 'data.yml')
        self.assertEqual(os.path.exists('data.yml'), True)

    def test_2_yaml_get_data(self,):
        yml_data = yaml_get_data('data.yml')
        self.assertEqual(self.d, yml_data)

