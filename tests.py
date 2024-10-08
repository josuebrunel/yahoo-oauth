from __future__ import absolute_import

import pytest

import os
import logging

import myql
from myql.utils import pretty_json

from yahoo_oauth.utils import write_data, get_data
from yahoo_oauth import  OAuth2

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s %(levelname)s] [%(name)s.%(module)s.%(funcName)s] %(message)s \n")
oauth_logger = logging.getLogger('yahoo_oauth')
oauth_logger.disabled = False


def test_oauth2():
    oauth = OAuth2(None, None, from_file='oauth2.yaml')
    response = oauth.session.get('https://fantasysports.yahooapis.com/fantasy/v2/games?format=json')
    logging.debug(pretty_json(response.content))
    assert response.status_code == 200


def test_oauth2_without_browser():
    oauth = OAuth2(None, None, from_file='oauth2.yaml', browser_callback=False)
    response = oauth.session.get('https://fantasysports.yahooapis.com/fantasy/v2/games?format=json')
    logging.debug(pretty_json(response.content))
    assert response.status_code == 200


@pytest.fixture
def data():
    return {
        'ck': 'consumer_key',
        'cs': 'consumer_secret'
    }


@pytest.fixture
def data_json():
    return 'data.json'


@pytest.fixture
def data_yaml():
    return 'data.yaml'


@pytest.fixture(params=['data_json', 'data_yaml'])
def data_format(request, data_json, data_yaml):
    return locals().get(request.param)


def test_write_data(data, data_format):
    write_data(data, data_format)
    assert os.path.exists(data_format)


def test_get_data(data, data_format):
    data_stored = get_data(data_format)
    assert data == data_stored

