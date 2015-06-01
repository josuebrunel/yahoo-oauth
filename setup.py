import os
from setuptools import setup, find_packages

__author__ = 'Josue Kouka'
__email__ = 'josuebrunel@gmail.com'
__version__ = "0.1.2"

#requirements.txt
with open('requirements.txt') as f:
  required = f.read().splitlines()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = "yahoo-oauth",
  version = __version__,
  description = "Python Yahoo OAuth Library",
  long_description = read("README.rst"),
  author = __author__,
  author_email = __email__,
  url = "https://github.com/josuebrunel/yahoo-oauth",
  download_url = "https://github.com/josuebrunel/yahoo-oauth/archive/{0}.tar.gz".format(__version__),
  keywords = ['yahoo','oauth'],
  packages = find_packages(),
  classifiers = [
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Development Status :: 5 - Stable',
    'Software Development :: Libraries :: Python Modules',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License'
  ],
  platforms=['Any'],
  license='MIT',
  install_requires = required
)
