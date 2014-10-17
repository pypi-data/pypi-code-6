#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
from drove.importer import Importer
from nose.tools import raises


def test_importer_default():
    """Testing Importer: from standard library"""
    importer = Importer("drove.data")
    cl = importer("value", "test", 1.0)
    assert cl.__class__.__name__ == 'Value'


def test_importer_path():
    """Testing Importer: from path"""
    path = os.path.join(os.path.dirname(__file__), "importer")
    importer = Importer(path=[path], class_suffix="Plugin")
    cl = importer("cpu", None, None)
    assert cl.__class__.__name__ == 'CpuPlugin'
    del sys.modules["cpu"]  # ensure that plugin is removed


@raises(ImportError)
def test_imported_noargs():
    """Testing Importer: missing arguments"""
    Importer()
