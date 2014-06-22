#!/usr/bin/env python
# -*- coding: utf-8 -*-


def write_file_contents(path, contents):
    with open(path, 'wb') as f:
        f.write(contents)

# vim: filetype=python
