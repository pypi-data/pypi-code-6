#!/usr/bin/env python
#
# Author: Paul D. Eden <paul@benchline.org>
# Created: 2014-04-30
"""
Script for reusable functions that help with freezing python code into binaries.
"""
import os
import sys

import benchline.args


def validate_args(parser, options, args):
    pass


def abs_res_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller

    >>> p = abs_res_path("binary.py")
    >>> p.endswith("binary.py")
    True
    >>> p.startswith("C") if os.name == 'nt' else p.startswith("/")
    True

    :param relative_path: string
    :return: string
    """
    if frozen_in_pyinstaller():
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def frozen_in_pyinstaller():
    """Let's you know if the currently executing code is executing out of pyinstaller or not
    :return: boolean
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        sys._MEIPASS
        return True
    except AttributeError:
        return False


def main():
    benchline.args.go(__doc__, validate_args=validate_args)


if __name__ == "__main__":
    main()
