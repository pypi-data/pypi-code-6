# -*- coding: utf-8 -*-
"""
    __init__

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool


def register():
    '''
        Register classes
    '''
    Pool.register(
        module='account_ca', type_='model'
    )
