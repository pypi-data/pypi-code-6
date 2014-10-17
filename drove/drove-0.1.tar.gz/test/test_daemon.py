#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
from nose.tools import raises
from nose.tools import with_setup
from drove.daemon import Daemon

_os = os.name


def _teardown():
    os.name = _os


@with_setup(teardown=_teardown)
@raises(NotImplementedError)
def test_daemon():
    """Testing Daemon: invalid platform"""
    os.name = 'foo'
    Daemon.create(lambda: None)
