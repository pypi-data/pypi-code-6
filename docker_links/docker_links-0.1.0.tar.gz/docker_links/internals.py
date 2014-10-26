# -*- coding: utf-8 -*-
import os
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


def docker_link(env_variable, overrides=None):
    if overrides is None:
        overrides = {}
    url = urlparse(os.environ.get(env_variable, ''))
    return _docker_link_helper(
        url_to_dict(url),
        overrides,
    )


def build_netloc(username, password, hostname, port):
    if not password:
        creds = "{username}"
    else:
        creds = "{username}:{password}"

    if not port:
        host = "{hostname}"
    else:
        host = "{hostname}:{port}"

    if not (username or password):
        return host.format(hostname=hostname, port=port)
    else:
        return (creds + "@" + host).format(
            username=username,
            password=password,
            hostname=hostname,
            port=port,
        )


def url_to_dict(url):
    return {
        "scheme": url.scheme,
        "netloc": url.netloc,
        "path": url.path,
        "query": url.query,
        "fragment": url.fragment,
        "username": url.username,
        "password": url.password,
        "hostname": url.hostname,
        "password": url.password,
    }


def dict_to_url(url_dict):
    return (
        url_dict["scheme"],
        build_netloc(
            url_dict["username"],
            url_dict["password"],
            url_dict["hostname"],
            url_dict["port"],
        ),
        url_dict["path"],
        url_dict["query"],
        url_dict["fragment"],
    )


def _docker_link_helper(url_dict, overrides):
    url_dict = url_dict.copy()  # Let's avoid mutation, shall we?
    url_dict.update(overrides)
    return urlparse.urlunsplit(dict_to_url(url_dict))
