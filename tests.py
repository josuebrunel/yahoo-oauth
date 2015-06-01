from __future__ import absolute_import

import unittest

import os

from yahoo_oauth import json_write_data, json_get_data

class testYahooOAuth(unittest.TestCase):
    """Class to tests Yahoo OAuth module
    """

    def setUp(self,):
        self.d = {'ck':'consumer_key','cs':'consumer_secret'} 

    def tearDown(self):
        os.unlink('test.json')

    def test_json_1_write_data(self,):
        json_write_data(self.d, 'test.json')
        self.assertEquals(os.path.exists('test.json'),True)

    def test_2_json_get_data(self,):
        json_data = json_get_data('test.json')
        self.assertEquals(self.d,json_data)
