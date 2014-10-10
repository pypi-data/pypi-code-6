# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

"""restarter command line interface."""


import logging
import optparse
import restarter
import restarter.app
import pkg_resources
import sys


def options():
    dist = pkg_resources.get_distribution('restarter')
    p = optparse.OptionParser(
        version='%prog '+dist.version,
        usage='%prog [OPTIONS] PIDFILE')
    p.description = 'Perform service restarts after updates'
    p.add_option('-r', '--restart', metavar='COMMAND',
                 help='shell command to restart service')
    p.add_option('-R', '--hard-restart', metavar='COMMAND',
                 help='shell command to perform hard restart if normal restart '
                 'has failed')
    p.add_option('-x', '--exclude', action='append', metavar='PATTERN',
                 help="ignore mmap'ed files mathing shell glob PATTERN in the "
                 "decision to restart")
    p.add_option('-d', '--delay', type='float', default=0,
                 help='wait DELAY seconds between restart command execution '
                 'and service startup verification')
    p.add_option('-f', '--fail', action='store_true',
                 help='fail if pidfile does not exist or process is not '
                 'running')
    p.add_option('-v', '--verbose', action='store_const', const=1,
                 dest='verbosity', default=0,
                 help='print more output')
    p.add_option('-q', '--quiet', action='store_const', const=-1,
                 dest='verbosity', help='print only error messages')
    options, args = p.parse_args()
    if len(args) != 1:
        p.error('need pid file')
    return args[0], options


def setup_logger(verbosity=0):
    l = logging.getLogger('restarter')
    ch = logging.StreamHandler()
    if verbosity < 0:
        ch.setLevel(logging.ERROR)
    elif verbosity > 0:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter('%(name)s: %(message)s'))
    l.addHandler(ch)


def main():
    pidfile, opts = options()
    setup_logger(opts.verbosity)
    app = restarter.app.App(pidfile, opts)
    try:
        restart_pending = app()
    except restarter.RestartError as e:
        print('restarter: ' + str(e), file=sys.stderr)
        sys.exit(1)
    if restart_pending:
        sys.exit(3)
