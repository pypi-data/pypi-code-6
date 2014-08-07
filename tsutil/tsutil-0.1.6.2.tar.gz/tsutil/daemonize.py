#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Turbidsoul Chen
# @Date:   2014-03-07 17:11:20
# @Last Modified by:   Turbidsoul Chen
# @Last Modified time: 2014-07-16 15:52:49


import os
import sys


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        pid = os.fork()
        print(pid)
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write('fork #1 failed: (%d) %s\n' % (e.errno, e.strerror))
        sys.exit(1)
    os.chdir('/')
    os.umask(0)
    os.setsid()
    try:
        pid = os.fork()
        print(pid)
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write('fork #2v failed: (%d) %s\n' % (e.errno, e.strerror))
        sys.exit(1)

    for f in sys.stdout, sys.stderr:
        f.flush()

    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stdout, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
