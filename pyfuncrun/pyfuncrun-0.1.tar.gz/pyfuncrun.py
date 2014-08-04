#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A tool to run a python function in a module from command line.

This tool import a function from command line arguments and run it.
It is helpful to test a function when you developing or just want
to run a function in module. If you want to test a function, please
use unittest instead of this tool.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import importlib


def import_attribute(name):
    """Return an attribute from a dotted path name (e.g. "path.to.func").

    I steal this function from RQ
    """
    module_name, attribute = name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attribute)


def main():
    """Entry function"""
    func_str = sys.argv[1]
    sys.argv = sys.argv[1:]
    func = import_attribute(func_str)
    func()


if __name__ == '__main__':
    main()
