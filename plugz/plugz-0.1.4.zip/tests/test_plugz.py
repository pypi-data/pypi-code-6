#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_plugz
----------------------------------

Tests for `plugz` module.
"""
import os

import pytest

import plugz
from plugz import errors, PluginTypeBase, StandardPluginType

def test_loading_plugins_without_correct_arguments():
    """ Loading Plugins without giving valid arguments should fail.

    Make sure this is actually the case by going through different
    scenarios regarding invalid plugin types.

    """
    # if None is passed as type, the according error needs to be raised
    with pytest.raises(errors.NoValidPluginTypeError):
        plugins = plugz.load_plugins([], None)

    # create class object that is not a valid type
    # because it does not inherit from the correct class
    class MyInvalidType():
        pass

    # if an invalid PluginType is given, the according error is raised
    with pytest.raises(errors.InvalidPluginTypeError):
        plugins = plugz.load_plugins([], MyInvalidType)

    class MyValidType(PluginTypeBase):
        pass

    # if no paths are given, raise the according error
    with pytest.raises(errors.NoPluginPathsProvided):
        plugins = plugz.load_plugins([], MyValidType)

    # if paths are given but one is invalid, raise the error
    with pytest.raises(errors.InvalidPluginPath):
        plugins = plugz.load_plugins(['/invalid/path/' ], MyValidType)


def test_loading_plugins_for_standard_plugin_type():
    """    """
    rel_path_tokens = ['data', 'plugins', 'standard', 'valid']
    valid_dir = os.path.join(os.path.dirname(__file__), *rel_path_tokens)
    plugins = plugz.load_plugins([valid_dir], StandardPluginType)

    assert len(plugins) == 2, \
           'Test did not find the two valid plugins in data. Found %s' % plugins

    # make sure the loaded plugins have the correct plugintype.
    assert all(map(lambda x: x.plugintype == StandardPluginType.plugintype, plugins))
    # make sure it's the correct plugins that were loaded.
    assert 'MyFirstValidPlugin' in [p.__name__ for p in plugins]
    assert 'MyValidPluginTwo' in [p.__name__ for p in plugins]

    for p in plugins:
        instance = p()
        instance.activate()
        # print 'Activated:', instance

    rel_path_tokens = ['data', 'plugins', 'standard', 'invalid']
    invalid_dir = os.path.join(os.path.dirname(__file__), *rel_path_tokens)
    plugins = plugz.load_plugins([invalid_dir], StandardPluginType)

    assert len(plugins) == 0 # they are all invalid
