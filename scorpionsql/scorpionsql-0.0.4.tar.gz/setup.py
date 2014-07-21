#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
from setuptools import setup, find_packages
import scorpionsql

setup(name="scorpionsql",
    version=scorpionsql.__version__,
    description="SQL-related and other shared packages used by scorpion and dbwipes",
    license="MIT",
    author="Eugene Wu",
    author_email="eugenewu@mit.edu",
    url="http://github.com/sirrice/scorpionsql",
    include_package_data = True,      
    packages = find_packages(),
    package_dir = {'scorpionsql' : 'scorpionsql'},
    scripts = [ ],
    package_data = {
      'scorpion': [
        'jars/scala-library.jar',
        'jars/sqlparser.jar'
      ]
    },
    install_requires = [
      'psycopg2', 'sqlalchemy', 'numpy', 'pyparsing'
    ],
    keywords= "")
