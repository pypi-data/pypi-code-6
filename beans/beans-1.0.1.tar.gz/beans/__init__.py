"""

The Beans Python Business Library

This module provides a wrapper around the Beans Business API, the
interface to the api is provided by the :py:class:`beans.Business`
object.

Copyright 2014 Beans
"""

__version__ = '1.0.1'

from .exception import BeansException

from .business import Business

business = None


def initialize(secret=None):
    global business
    business = Business(secret)
    business.version = __version__


class REWARD_TYPE(object):
    """
    Lists reward type
    Use this class to treat your reward accordingly to the type.
    """
    CART_COUPON = 'CART_COUPON'
    CART_DISCOUNT = 'CART_DISCOUNT'


