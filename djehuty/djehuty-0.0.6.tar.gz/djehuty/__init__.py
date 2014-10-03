# -*- coding: utf-8 -*-

from pkg_resources import get_distribution, DistributionNotFound
import os.path

try:
    _dist = get_distribution('foobar')
    if not __file__.startswith(os.path.join(_dist.location, 'djehuty')):
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'not installed'
else:
    __version__ = _dist.version


def includeme(config):

    config.include('cornice')
