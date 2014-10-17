#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import drove.log
from drove.log import logging


def test_log_getdefaultlogger():
    """Testing log: getDefaultLogger()"""
    assert drove.log.getDefaultLogger() == logging.getLogger("drove.default")


def test_log_socket():
    """Testing AppLogger: get_syslog_socket()"""
    import sys
    log = drove.log.AppLogger()

    sys.platform = "linux2"
    assert log.get_syslog_socket() == "/dev/log"

    sys.platform = "freebsd"
    assert log.get_syslog_socket() == "/var/run/log"

    sys.platform = "darwin"
    assert log.get_syslog_socket() == "/var/run/syslog"

    sys.platform = "unknown"
    assert log.get_syslog_socket() == "/dev/log"
    del sys


def test_log_applogger_syslog():
    """Testing AppLogger: syslog"""
    log = drove.log.AppLogger(syslog=True)
    assert "SysLogHandler" in [x.__class__.__name__ for x in log.handlers]


def test_log_applogger_logfile():
    """Testing AppLogger: logfile"""
    log = drove.log.AppLogger(logfile="/dev/null")
    assert "RotatingFileHandler" in \
        [x.__class__.__name__ for x in log.handlers]


def test_log_applogger_console():
    """Testing AppLogger: console"""
    log = drove.log.AppLogger(console=True)
    assert "StreamHandler" in \
        [x.__class__.__name__ for x in log.handlers]
