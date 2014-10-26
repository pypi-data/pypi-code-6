from setuptools import setup

setup(name='pgconn',
      version='0.1',
      scripts=['bin/pgconn'],
      description='Utility to connect to your Postgres DB using your .pgpass file',
      url='http://github.com/dhydrated/pgconn',
      author='Taufek Johar',
      author_email='dhydrated@gmail.com',
      license='MIT',
      packages=['pgconn'],
      zip_safe=False)