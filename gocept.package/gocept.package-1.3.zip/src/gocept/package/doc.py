# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import os
import os.path
import pkg_resources
import sys


def main(argv=sys.argv):
    builder = 'html'
    output_dir = 'doc'
    if len(argv) > 1 and argv[1] == '--pdf':
        argv.pop(1)
        builder = 'latex'
        output_dir = 'pdf'
    cwd = os.getcwd()
    sphinx_build = pkg_resources.load_entry_point(
        'Sphinx', 'console_scripts', 'sphinx-build')
    argv = ['sphinx-build'] + argv[1:]
    source_dir = os.path.join(cwd, 'doc')
    output_dir = os.path.join(cwd, 'build', output_dir)
    argv += ['-E', '-b', builder, source_dir, output_dir]
    sphinx_build(argv)
    if builder == 'latex':
        os.system('make -C %s all-pdf' % output_dir)
