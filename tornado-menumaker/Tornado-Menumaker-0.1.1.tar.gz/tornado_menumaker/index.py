#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""

from .route import Route

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '26.06.13 - 14:25'


class IndexRoute(Route):
    """
        A Index Route
    """

    def __init__(self, url: str='/index', **kwargs):
        super().__init__(url=url, kwargs=kwargs)

    @classmethod
    def isindex(cls, other: object) -> bool:
        """
            Is other an instance of IndexRoute?

            :param other: Object to compare
        """
        return isinstance(other, cls)