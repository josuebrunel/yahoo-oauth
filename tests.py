import unitttest

import os

from yahoo_ouath import write_json_data, get_json_data

class testYahooOAuth(unittest.TestCase):
    """Class to tests Yahoo OAuth module
    """

    def setUp(self,):
        pass

    def tearDown(self):
        os.unlink('test.json')

    def test_wirte_json_data(self,):
        d = {'ck':'consumer_key','cs':'consumer_secret'}
        write_json_data(d, 'test.json')
        self.assertEquals(os.path.exists('test.json'),True)

    def test_get_json_data(self,):
        pass
