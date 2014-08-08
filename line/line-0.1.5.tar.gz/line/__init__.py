# -*- coding: utf-8 -*-
"""
    line 
    ~~~~

    May the LINE be with you...

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""
from .client import LineClient
from .models import LineGroup, LineContact, LineRoom

__copyright__ = 'Copyright 2014 by Taehoon Kim'
__version__ = '0.1.5'
__license__ = 'BSD'
__author__ = 'Taehoon Kim'
__author_email__ = 'carpedm20@gmail.com'
__url__ = 'http://github.com/carpedm20/line'

__all__ = [
    # LineClient object
    'LineClient',
    # model wrappers for LINE API
    'LineGroup', 'LineContact', 'LineRoom',
]
