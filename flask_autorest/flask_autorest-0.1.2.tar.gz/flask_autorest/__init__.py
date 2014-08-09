# -*- coding: utf-8 -*-
"""
AUTOREST_SOURCES:
    {
        'test': {
            'uri': 'mysql://root:@localhost/test_stat',
            'engine_kwargs': {
                'pool_size': 1,
                'pool_recycle': -1,
                'max_overflow': 0,
            },
            'auth': ('admin', 'admin'),
            'tables': {
                    'user': {
                        'per_page': 10,
                        'max_per_page': 100,
                    }
                },
            }
        }
    }
AUTOREST_BLUEPRINT_NAME
AUTOREST_URL_PREFIX

"""

__version__ = '0.1.2'

from .autorest import AutoRest
