# -*- coding: utf-8 -*-


"""Functions returning an IMAP account state

Usage: listdir [options]

    -c, --config-file=<FILE>    Configuration file (`~/.config/imap-cli` by default)
    -f, --format=<FMT>          Output format
    -v, --verbose               Generate verbose messages
    -h, --help                  Show help options.
    --version                   Print program version.
----
imap-cli-listdir 0.1.0
Copyright (C) 2014 Romain Soufflet
License MIT
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
"""


from docopt import docopt
import logging
import os
import sys

from imap_cli import config, helpers


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

DEFAULT_CONFIG_FILE = '~/.config/imap-cli'


def main():
    args = docopt(__doc__[2:], version='IMAP-Cli Status v0.1')
    logging.basicConfig(
        level=logging.DEBUG if args['--verbose'] else logging.WARNING,
        stream=sys.stdout,
    )

    config_filename = args['--config-file'] or DEFAULT_CONFIG_FILE
    config_filename = os.path.abspath(os.path.expanduser(os.path.expandvars(config_filename)))
    log.debug("Using configuration file '{}'".format(config_filename))

    ctx = config.new_context(config_filename)
    helpers.connect(ctx)
    for tags, path, dirname in helpers.list_dir(ctx):
        print dirname[1:-1]


if __name__ == '__main__':
    sys.exit(main())
