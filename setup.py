import os
from setuptools import setup, find_packages

__author__ = 'Josue Kouka'
__email__ = 'josuebrunel@gmail.com'
__version__ = '0.1.9'

#requirements.txt
with open('requirements.txt') as f:
  required = f.read().splitlines()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = "yahoo_oauth",
  version = __version__,
  description = "Python Yahoo OAuth Library. Supports OAuth1 and OAuth2",
  long_description = read("README.rst"),
  author = __author__,
  author_email = __email__,
  url = "https://github.com/josuebrunel/yahoo-oauth",
  download_url = "https://github.com/josuebrunel/yahoo-oauth/archive/{0}.tar.gz".format(__version__),
  keywords = ['yahoo','oauth','oauth1', 'oauth2'],
  packages = find_packages(),
  classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Development Status :: 5 - Production/Stable',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License'
  ],
  platforms=['Any'],
  license='MIT',
  install_requires = required
)
