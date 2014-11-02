import re
import functools

from django.contrib.admindocs.views import simplify_regex
from django.core.exceptions import ViewDoesNotExist
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver


def get_urls(patterns, sort=False):
    urls = []
    views = get_views(patterns)

    for (func, regex, url_name) in views:
        if isinstance(func, functools.partial):
            func = func.func

        func_name = get_name(func)

        urls.append(dict(
            view="{0}.{1}".format(func.__module__, func_name),
            name=url_name or "",
            path=simplify_regex(regex),
        ))

    if sort:
        urls = sorted(urls, key=lambda x: x["path"])

    return urls


def get_name(func):
    if hasattr(func, "__name__"):
        return func.__name__
    elif hasattr(func, "__class__"):
        return "%s()" % func.__class__.__name__
    else:
        return re.sub(r" at 0x[0-9a-f]+", "", repr(func))


def get_views(patterns, base=""):
    """
    Return views from a list of patterns.

    Each object in the returned list is a two-tuple: (view_func, regex)
    """
    views = []

    for p in patterns:
        if isinstance(p, RegexURLPattern):
            try:
                views.append((p.callback, base + p.regex.pattern, p.name))
            except ViewDoesNotExist:
                continue
        elif isinstance(p, RegexURLResolver):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(get_views(patterns, base + p.regex.pattern))
        elif hasattr(p, "_get_callback"):
            try:
                views.append(
                    (p._get_callback(), base + p.regex.pattern, p.name),
                )
            except ViewDoesNotExist:
                continue
        elif hasattr(p, "url_patterns") or hasattr(p, "_get_url_patterns"):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(get_views(patterns, base + p.regex.pattern))
        else:
            raise TypeError(
                "%s does not appear to be a url pattern" % p,
            )
    return views
