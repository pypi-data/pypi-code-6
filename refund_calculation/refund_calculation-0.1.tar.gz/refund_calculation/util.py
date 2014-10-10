from __future__ import absolute_import

__all__ = ('zip',)


try:
    from itertools import izip
    zip = izip
except ImportError:
    zip = zip
