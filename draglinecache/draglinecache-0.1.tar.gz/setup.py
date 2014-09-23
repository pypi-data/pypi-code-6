try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='draglinecache',
      version='0.1',
      description='Caching interface for dragline',
      author='Ashwin Rajeev',
      author_email='ashwin@inzyte.com',
      url='http://www.inzyte.com',
      packages=['draglinecache'],
      install_requires=['pymongo']
      )
