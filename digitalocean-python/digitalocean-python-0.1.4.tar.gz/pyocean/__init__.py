# encoding: utf-8

"""
PyOcean
=======
Python wrapper for the DigitalOcean API v2. Sample usage:

    >>> import pyocean
    >>> digitalocean = pyocean.DigitalOcean('YOUR_ACCESS_TOKEN')
    >>> for droplet in digitalocean.droplet.all():
    ...     print(droplet)

"""

import os

from .domain import Domain, DomainIterator
from .domainrecord import DomainRecord, DomainRecordIterator
from .droplet import Droplet, DropletIterator
from .image import Image, ImageIterator
from .action import Action, ActionIterator
from .key import Key, KeyIterator
from .size import Size, SizeIterator
from .region import Region, RegionIterator


class DigitalOcean(object):
    """This class serves as the entry point to the pyocean package.
    """

    def __init__(self, access_token):
        self.access_token = access_token
        os.environ['PYOCEAN_ACCESS_TOKEN'] = access_token

    def __getattr__(self, attr):
        """Convenient method to instantiate the classes.
        """
        if attr == 'domain':
            return Domain()
        elif attr == 'droplet':
            return Droplet()
        elif attr == 'image':
            return Image()
        elif attr == 'action':
            return Action()
        elif attr == 'size':
            return Size()
        elif attr == 'region':
            return Region()
        elif attr == 'ssh_key':
            return Key()
        else:
            me = self.__class__.__name__
            raise AttributeError("'%s' object has no attribute '%s'" % (me, attr))
