# -*- coding: utf-8 -*-

from voluptuous import Required

from ..request import TransactionMethod


class ThreeDRedirect(TransactionMethod):
    """
    Starts 3DS redirect process.
    """
    def __init__(self, **kwargs):
        """
        :param order_id: order_id that is in 3DS wait order status
        """
        super(ThreeDRedirect, self).__init__(**kwargs)

    __name__ = 'three_d_redirect'
    schema = {Required('order_id'): int}