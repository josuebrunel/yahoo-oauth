# yahoo_oauth

[![Build Status](https://travis-ci.org/josuebrunel/yahoo-oauth.svg?branch=master)](https://travis-ci.org/josuebrunel/yahoo-oauth)
[![Documentation Status](https://readthedocs.org/projects/yahoo-oauth/badge/?version=latest)](https://readthedocs.org/projects/yahoo-oauth/?badge=latest)
[![Code Health](https://landscape.io/github/josuebrunel/yahoo-oauth/master/landscape.svg?style=flat)](https://landscape.io/github/josuebrunel/yahoo-oauth/master)
[![PyPI](https://img.shields.io/pypi/v/yahoo-oauth.svg?style=flat)](https://pypi.python.org/pypi/yahoo_oauth)
[![PyPI](https://img.shields.io/pypi/dm/yahoo-oauth.svg?style=flat)](https://pypi.python.org/pypi/yahoo_oauth)
[![PyPI](https://img.shields.io/pypi/pyversions/yahoo-oauth.svg?style=flat)](https://pypi.python.org/pypi/yahoo_oauth)
[![PyPI](https://img.shields.io/pypi/implementation/yahoo-oauth.svg?style=flat)](https://pypi.python.org/pypi/yahoo_oauth)
[![Coverage Status](https://coveralls.io/repos/josuebrunel/yahoo-oauth/badge.svg?branch=master)](https://coveralls.io/r/josuebrunel/yahoo-oauth?branch=master)
[![PyPI](https://img.shields.io/pypi/l/yahoo-oauth.svg?style=flat)](https://pypi.python.org/pypi/yahoo_oauth)

Yahoo_OAuth is a very easy to use OAuth library for Yahoo! APIs. 

## Installation

```python
pip install yahoo_oauth
```

## Quickstart

Only **2** parameters are required to get started

* ___consumer_key___ 
* ___consumer_secret___

I recommend putting those two into a file. Only ***json*** and ***yaml*** files are supported 

```json
{
    "consumer_key": "my_very_long_and_weird_consumer_key",
    "consumer_secret": "my_not_that_long_consumer_secret"
}
```

Once you acquired your access_token, this file will look like :

* **OAuth2**

```json
{
    "access_token": "DELvMgOYvwPQJS8eFW_2hRN5rJxz6dnHAOk2s.qB0iMIeRg5.ZpW3xZF0p8CABLjZ2gfNdE602dCN2wTHdGHHLtChF3ls9BUuZ1QDdqIVq.yWclfweleyZSq6dAzlPEHiskWmfItjHK5VERY_LONG_ACCESS_TOKEN_oyyD4cIKvdNJsJ9k779mAUqN02_5ugBeDfCLebqjL8uVuunObew0ERa2MxE6jywNY0TTCe9W0nqTd6n0lKoN4PSP1Dw_Ifwx6enGuhUUAhhpa7nNMyhNy_pe6PfDf7IJ5gbkdtw3mD1o2T218ZTV0owdrKDLSF9oZrNvZ75xDlqaaI5yeW_.L63zk11PjsWUd5K8LGhWSTgRbyhffCDBcqVwTYEqHwCyVqHX4z2kgHhGsc0ies6WMG33kSw5Cgun0fnPbdDuHBgQziXU.GMv4hIDoIDMSLGpzpcpkyx4GS1CC_RUQwKxLilR3MQy7X2gI3cJA4lhRPlXEOdhS5HIQiQTgMWO9nWt7.RR7XtXVg-",
    "consumer_key": "dj0yJmk9eFJINERDYWMY_CONSUMER_KEYmRGTnpZbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1iNQ--",
    "consumer_secret": "08802b459ab48eeaMY_CONSUMER_SECRET_0af6a4b75789f7",
    "guid": "AJHDHJMYGUID",
    "refresh_token": "APIENFXij.bjFW1tEcr2THE_REFRESH_TOKEN_Xn.4.DOIYOR37",
    "token_time": 1433553339.706037,
    "token_type": "bearer"
}
```

With that you should be good to go.

Normally, once your got all that, you can ***use the same credentials FOREVER***, you just have to ***REFRESH THEM***. 

## Examples

### OAuth2

```python
from yahoo_oauth import OAuth2
oauth = OAuth2(None, None, from_file='oauth2.json')
...

if not oauth.token_is_valid():
    oauth.refresh_access_token()
# Example
response = oauth.session.get(url, params=payload)
```

### Tips

* How to get your Global Unique Identifier (GUID)
```python
from yahoo_oauth import OAuth2

oauth = OAuth2('consumer_key', 'consumer_secret')
guid = oauth.guid

```

* How to disable **Yahoo_OAuth Logger**
```python
import logging
oauth_logger = logging.getLogger('yahoo_oauth')
oauth_logger.disabled = True
```

## Contribute

Any kind of contribution is welcomed.

0. report bug by opening an issue
1. Fork the repository
2. Make your changes
3. Test your changes
4. Submit a pull request

Have fun guys :wink:
