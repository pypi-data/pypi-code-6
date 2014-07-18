# -*- coding: utf-8 -*-
'''
Created on:    Nov 10, 2013
@author:        vahid
'''
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from isass.helpers import get_source_dirs, get_source_files, distinct, split_paths, minify
from isass import SassCompiler
import os.path
from isass.manifest import Manifest
import sys
import traceback


class IsassEventHandler(FileSystemEventHandler):
    extension = '.sass'

    def __init__(self, outfiles, dirs, files=None, lib_dirs = None):
        self.outfiles = outfiles
        self.dirs = dirs
        self.lib_dirs = lib_dirs if lib_dirs else []
        self.source_files = get_source_files(self.dirs,extension=self.extension)
        if files:
            self.source_files += files
        super(FileSystemEventHandler, self).__init__()

    def write_out(self):
        try:
            lib_dirs = get_source_dirs(self.dirs)
            if self.lib_dirs:
                lib_dirs += self.lib_dirs
            lib_dirs = distinct(lib_dirs)

            compiler = SassCompiler(lib_dirs=lib_dirs)
            for sf in self.source_files:
                print "Reading %s" % os.path.abspath(sf)
                compiler.read_file(sf)


            normal_output = compiler.get_css()
            if 'normal' in self.outfiles:
                normal_out_filename = os.path.abspath(self.outfiles['normal'])
                print "Writing %s" % normal_out_filename
                with open(normal_out_filename, 'w') as of:
                    of.write(normal_output)

            if 'minified' in self.outfiles:
                minified_out_filename = os.path.abspath(self.outfiles['minified'])
                print "Writing %s" % minified_out_filename
                with open(minified_out_filename, 'w') as of:
                    of.write(minify(normal_output))

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def on_any_event(self, event):
        paths = []
        if hasattr(event, 'src_path'):
            paths += split_paths(event.src_path)
        if hasattr(event, 'dest_path'):
            paths += split_paths(event.dest_path)

        changed = False
        for p in paths:
            if p in self.source_files:
                changed = True
                break

            if os.path.abspath(os.path.dirname(p)) in self.lib_dirs and p.endswith(self.extension):
                changed = True
                break

        if changed:
            # One or more sass file changes, trying to regenerate output
            self.write_out()


class SassObserver(Observer):

    def add_output(self, outfiles, dirs=None, files=None, lib_dirs=None):

        if isinstance(outfiles, basestring):
            outfiles = {'normal': outfiles}

        if dirs is None:
            dirs = []

        if files is None:
            files = []

        if lib_dirs is None:
            lib_dirs = []

        dirs = distinct(split_paths(dirs))

        handler = IsassEventHandler(outfiles, dirs, files=files, lib_dirs=lib_dirs)
        watch_dirs = list(dirs)

        if lib_dirs:
            watch_dirs += split_paths(lib_dirs)
        if files:
            watch_dirs += split_paths([os.path.dirname(p) for p in files])

        watch_dirs = [wd for wd in distinct(watch_dirs) if os.path.exists(wd)]

        handler.write_out()
        for d in watch_dirs:
            self.schedule(handler, d, recursive=False)

    def add_manifest(self, manifest):
        manifest = Manifest(manifest)
        for taskname in manifest.get_task_names():
            task = manifest[taskname]
            dirs = []
            files = []
            for s in task.sources:
                if os.path.isfile(s):
                    files.append(s)
                else:
                    dirs.append(s)
            self.add_output(outfiles=task.output,
                            dirs=dirs,
                            files=files,
                            lib_dirs=task.libdirs)
