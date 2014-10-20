#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pyautocad import Autocad

acad = Autocad()
acad.app.Documents.Open(os.path.realpath("test.dwg"))
# test.dwg = some existing file in current folder, or it can be full path
# os.path.realpath needed because Autocad accepts full path
