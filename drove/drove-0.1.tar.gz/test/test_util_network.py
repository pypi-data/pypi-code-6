#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import socket
import drove.util.network
from nose.tools import raises


def test_parse_addr():
    """Testing util.network: parse_addr() basic behaviour"""
    assert drove.util.network.parse_addr("127.0.0.1:12", resolve=False) == \
        ("127.0.0.1", 12, socket.AF_INET)

    assert drove.util.network.parse_addr("127.0.0.1", defport=12) == \
        ("127.0.0.1", 12, socket.AF_INET)

    assert drove.util.network.parse_addr("[::1]:12") == \
        ("::1", 12, socket.AF_INET6)

    assert drove.util.network.parse_addr("[::1]", defport=12) == \
        ("::1", 12, socket.AF_INET6)

    assert drove.util.network.parse_addr("localhost:12") in [
        ("::1", 12, socket.AF_INET6), ("127.0.0.1", 12, socket.AF_INET)]


@raises(ValueError)
def test_parse_addr_empty():
    """Testing util.network: parse_addr() empty address"""
    drove.util.network.parse_addr("")


@raises(ValueError)
def test_parse_addr_fail():
    """Testing util.network: parse_addr() bad address"""
    drove.util.network.parse_addr("300.0.0.1:12")


def _mocked_getaddrinfo(*args, **kwargs):
    return None


@raises(ValueError)
def test_parse_addr_fail_resolve():
    """Testing util.network: parse_addr() cannot resolve"""
    drove.util.network.socket.getaddrinfo = _mocked_getaddrinfo
    drove.util.network.parse_addr("127.0.0.1:12")


def test_getfqdn():
    """Testing util.network: getfqdn()"""
    x = drove.util.network.getfqdn
    x.reload()
    assert isinstance(str(x), str)
