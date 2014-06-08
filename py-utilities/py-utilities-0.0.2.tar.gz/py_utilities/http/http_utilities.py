#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import sys
import urllib2


def get(url, output=sys.stdout):
    response = urllib2.urlopen(url)
    shutil.copyfileobj(response, output)

# vim: filetype=python
