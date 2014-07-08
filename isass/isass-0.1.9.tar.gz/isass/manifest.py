# -*- coding: utf-8 -*-
'''
Created on:    Apr 1, 2014
@author:        vahid
'''
from pymlconf import ConfigManager, ConfigList, ConfigDict
from isass.helpers import get_source_dirs, get_source_files, distinct, minify
from isass import SassCompiler
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

    def process_task(self, taskname, extension=".sass"):
        task = self[taskname]
        dirs = []
        files = []
        for s in task.sources:
            if os.path.isfile(s):
                files.append(s)
            else:
                dirs.append(s)
        lib_dirs = get_source_dirs(dirs)
        if lib_dirs:
            lib_dirs += lib_dirs
        lib_dirs = distinct(lib_dirs)

        source_files = get_source_files(dirs,extension=extension)
        if files:
            source_files += files

        compiler = SassCompiler(lib_dirs=lib_dirs)
        for sf in source_files:
            print "Reading %s" % os.path.abspath(sf)
            compiler.read_file(sf)


        normal_output = compiler.get_css()

        if isinstance(task.output, basestring):
            task.output = {'normal': task.output}

        if 'normal' in task.output:
            normal_out_filename = os.path.abspath(task.output['normal'])
            print "Writing %s" % normal_out_filename
            with open(normal_out_filename, 'w') as of:
                of.write(normal_output)

        if 'minified' in task.output:
            minified_out_filename = os.path.abspath(task.output['minified'])
            print "Writing %s" % minified_out_filename
            with open(minified_out_filename, 'w') as of:
                of.write(minify(normal_output))

    def write_outputs(self):
        for taskname in self.get_task_names():
            self.process_task(taskname)
