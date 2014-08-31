#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from jinja2 import Environment
from jinja2 import FileSystemLoader
import logging
import os
from py_configurator.backends import get_provider
from py_configurator.config import Config
from py_skeleton.utilities import iter_files_filter
from py_skeleton.utilities import render_template_to_target
from py_skeleton.utilities import resolve_templated_file_path
import sys
import traceback

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def init_argparser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c', '--config', action='store',
                        help='template configuration data', required=True)
    parser.add_argument('-s', '--source', action='store',
                        help='template source', required=True)
    parser.add_argument('-d', '--destination', action='store',
                        help='destination', required=True)
    parser.add_argument('-e', '--ext', action='store',
                        help='template extension', default=".tmpl")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase chattiness of script')
    return parser


def do_work_son(args):
    loader = FileSystemLoader(args.source)
    env = Environment(loader=loader, keep_trailing_newline=True)
    config = Config(get_provider(args.config))

    for file in iter_files_filter(args.source, "*{0}".format(args.ext)):
        src = file.replace(args.source, "")
        target = resolve_templated_file_path(src, config)

        render_template_to_target(
            env,
            src,
            config.to_dict(),
            os.path.join(args.destination, target),
            args.ext)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = init_argparser()
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    try:
        do_work_son(args)
    except:
        trace = traceback.format_exc()
        logging.error("OMGWTFBBQ: {0}".format(trace))
        sys.exit(1)

    # Yayyy-yah
    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

# vim: filetype=python
