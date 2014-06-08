# -*- coding: utf-8 -*-
from loading import load_plugins, register_plugin
from plugz import PluginTypeBase
from plugintypes import StandardPluginType

__author__ = 'Matti Gruener'
__email__ = 'matti@mistermatti.com'
__version__ = '0.1.1'

__ALL__ = [load_plugins, register_plugin, StandardPluginType, PluginTypeBase]
