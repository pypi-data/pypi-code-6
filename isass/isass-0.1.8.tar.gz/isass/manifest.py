# -*- coding: utf-8 -*-
'''
Created on:    Apr 1, 2014
@author:        vahid
'''
from pymlconf import ConfigManager, ConfigList, ConfigDict

import os.path



class Manifest(ConfigManager):
    def __init__(self,manifest_file):
        ConfigManager.__init__(self, files=manifest_file)
        manifest_dir = os.path.dirname(manifest_file)
        for key in self.get_task_names():
            manifest_config = self[key]
            manifest_config.sources = [i if i.startswith('/') else os.path.abspath(os.path.join(manifest_dir, i)) for i in manifest_config.sources]

            if hasattr(manifest_config,'libdirs'):
                manifest_config.libdirs = [i if i.startswith('/') else os.path.abspath(os.path.join(manifest_dir, i)) for i in manifest_config.libdirs]
            else:
                manifest_config.libdirs = ConfigList()

            if isinstance(manifest_config.output, basestring):
                manifest_config.output = ConfigDict({'normal': manifest_config.output})

            for k, v in manifest_config.output.items():
                if not v.startswith('/'):
                    manifest_config.output[k] = os.path.abspath(os.path.join(manifest_dir, v))

    def get_task_names(self):
        for k in self.keys():
            if isinstance(k,basestring) and not k.startswith('_'):
                yield k