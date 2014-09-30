#from setuptools import setup
import os
from distutils.core import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = 'pyproms',
    packages = ['pyproms'],
    version = '1.1',
    author = 'Nicholas Car',
    author_email = 'nicholas.car@csiro.au',
    url = 'https://github.com/ncar/pyproms',
    download_url = 'https://github.com/ncar/pyproms/tarball/1.1',
    license = 'LICENSE.txt',
    description = 'PyPROMS is a client library to make PROV and PROMS documents and submit them to a PROMS server instance',
    keywords = ['rdf', 'prov', 'prov-o', 'proms', 'proms-o', 'provenance'],
    long_description = read('README.md'),
    install_requires = ['rdflib >= 3.0.0'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
)
