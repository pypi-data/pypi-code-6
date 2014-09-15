#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""

"""
from itertools import groupby
from types import FunctionType

from .route import Route
from .index import IndexRoute
from .page import Page

__author__ = 'Martin Martimeo <martin@martimeo.de>'
__date__ = '16.06.13 - 21:45'

_pages = []
_routes = []


def page(url: str, caption: str, **kwargs):
    """
        Decorate a handler to act as a menumaker page

        :param url: Prefix for all routes of this handler
        :param caption: Caption of the page
        :param kwargs: Additional arguments
    """
    page = Page(url=url, caption=caption, **kwargs)
    _pages.append(page)
    return page


def index(function: FunctionType):
    """
        Decorate method as index route (will be available via page.url)

        :param function: Body
    """
    index = IndexRoute()(function)
    _routes.append(index)
    return index


def indexpage(url: str, caption: str=None, **kwargs):
    """
        Route for the index

        :param url: Url of the indexpage (will be prefixed with page.url)
        :param caption: Caption of the menu item (if omitted only route will be created)
        :param kwargs: Additional arguments
    """
    route = IndexRoute(url=url, caption=caption, **kwargs)
    _routes.append(route)
    return route


def subpage(url: str, caption: str=None, **kwargs):
    """
        Route for a subpage

        :param url: Url of this subpage (will be prefixed with page.url)
        :param caption: Caption of the menu item (if omitted only route will be created)
        :param kwargs: Additional arguments
    """
    route = Route(url=url, caption=caption, **kwargs)
    _routes.append(route)
    return route


def routes():
    """
        Return all registered routes
    """
    return _routes + _pages


def items(check: str='caption'):
    """
        Return all elements in ordered menu tree structure

        yields level, url, kwargs[check], subroutes, kwargs

        :param check: Check for existant of this keyword in kwargs when yelling
    """

    def _items(top: int, lroutes: list):
        def _key(route: Route) -> str:
            return '/'.join(route.url.split('/')[:top + 1])

        for name, routes in groupby(lroutes, key=_key):
            routes = list(routes)
            if len(routes) == 0:
                return []
            elif len(routes) == 1:
                route = routes[0]
                if not check in route.kwargs or route.kwargs[check] is None:
                    continue
                yield top, route.url, route.kwargs[check], [], route.kwargs
            elif routes[0].url == name:
                route = routes[0]
                if not check in route.kwargs or route.kwargs[check] is None:
                    yield from _items(top + 1, routes[1:])
                else:
                    yield top, route.url, route.kwargs[check], _items(top + 1, routes[1:]), route.kwargs
            else:
                yield from _items(top + 1, routes)

    yield from _items(1, _pages + _routes)

