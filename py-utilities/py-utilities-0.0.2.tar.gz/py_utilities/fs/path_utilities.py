#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ntpath
import os


def expanded_abspath(dir):
    expanded = os.path.expanduser(os.path.expandvars(dir))
    return os.path.abspath(expanded)


def filename(path):
    """ Returns filename in path """
    dirs, f = ntpath.split(path)
    return f or ntpath.basename(dirs)


def get_first_dir_path(dir_paths):
    """
    Returns the first valid dir path in dir_paths
    """
    return _get_first_in_path(dir_paths, lambda path: os.path.isdir(path))


def get_first_file_path(file_paths):
    """
    Returns the first valid file path in file_paths
    """
    return _get_first_in_path(file_paths, lambda path: os.path.isfile(path))


def _get_first_in_path(paths, function):
    """
    Returns the first found path in paths that function resolves
    """
    found = [path for path in paths if function(path)]
    return found[0] if len(found) > 0 else None

# vim: filetype=python
