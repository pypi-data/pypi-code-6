#!/usr/bin/env python

from distutils.core import setup
ld = """
Caching JSON REST API Get Queries
=================================

I wrote this so I could stop abusing people's REST APIs whenever I was
developing tools. Currently this will only cache GET requests, and
nothing else. If you want more features, let me know!

Quick Usage:

::

    from restcache import QueryCache
    qc = QueryCache()
    qc.json_query('https://bitbucket.org/api/1.0/repositories/galaxy/galaxy-central/tags/')

The ``json_query`` call makes a ``urllib2`` request, and stores it in
``.cache/{base64 encoded url}``.

On initialization, QueryCache will check through the cache directory and
load any files.
"""

setup(name='restcache',
      version='1.1',
      description='Python REST API Cache',
      author='Eric Rasche',
      author_email='rasche.eric@yandex.ru',
      packages=['restcache'],
      long_description=ld,)
