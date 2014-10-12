# -*- coding: utf-8 -*-

import os
import re

from ..libraries.mod_pbxproj import XcodeProject

from cliff.command import Command
from clint.textui import colored, puts, progress

IGNORE_DIR_SUFFIX = ('.framework', '.embeddedframework', '.bundle', '.xcodeproj')

class Xcodeproj(Command):
    def get_parser(self, prog_name):
        parser = super(Xcodeproj, self).get_parser(prog_name)
        subparsers = parser.add_subparsers()

        fix_parser = subparsers.add_parser('check')
        fix_parser.add_argument('command', nargs='?', default='fix')
        fix_parser.add_argument('-p', '--project', type = str, help = 'the project to fix')

    def take_action(self, parsed_args):
        command = parsed_args.command

        if command == 'check':
            return self.check(parsed_args)

    def check(self, parsed_args):
        source = parsed_args.project
        pbxproj = self.find_pbxproj(source)
        resources = []

        if not pbxproj:
            puts(colored.red('.xcodeproj not found.'))
            return

        #get all resource
        for root, subdirs, files in os.walk(source):
            if self.is_spefical_dir(root):
                resources.append(os.path.basename(root))

            if self.is_in_ignore_dir(root, source):
                continue

            for f in files:
                if self.is_igore_file(os.path.basename(f)):
                    continue

                resources.append(os.path.basename(f))

        resources = list(set(resources))
        resources.sort()

    def find_pbxproj(self, path):
        pbxproj = None
        for subdir in os.listdir(path):
            ext = os.path.splitext(subdir)
            if ext[1] == '.xcodeproj':
                pbxproj = os.path.join(path, subdir, 'project.pbxproj')

        return XcodeProject.Load(pbxproj) if pbxproj else None

    def is_in_ignore_dir(self, path, root):
        is_ignore = False
        path = os.path.dirname(path)

        while path != root and not is_ignore:
            ext = os.path.splitext(path)[1] if len(os.path.splitext(path)) > 1 else None
            if not ext:
                continue
            basename = os.path.basename(path)
            is_ignore = ext in IGNORE_DIR_SUFFIX
            path = os.path.dirname(path)

        return is_ignore

    def is_framework_or_bundle(self, path):
        ext = os.path.splitext(path)[1] if len(os.path.splitext(path)) > 1 else None
        return ext and ext in IGNORE_DIR_SUFFIX

    def is_dylib(self, path):
        ext = os.path.splitext(path)[1] if len(os.path.splitext(path)) > 1 else None
        return ext and ext in ['.dylib']

    def is_igore_file(self, filename):
        pattern = r'^(Default|Icon)'
        return not not re.search(pattern, filename)
