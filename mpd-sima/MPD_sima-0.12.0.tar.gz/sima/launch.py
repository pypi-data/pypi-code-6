# -*- coding: utf-8 -*-
# Copyright (c) 2013, 2014 Jack Kaliko <kaliko@azylum.org>
#
#  This file is part of sima
#
#  sima is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  sima is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with sima.  If not, see <http://www.gnu.org/licenses/>.
#
#
"""Sima
"""

# standard library import
import logging
import sys

from importlib import __import__
from os.path import isfile
##

# third parties components
##

# local import
from . import core, info
from .lib.logger import set_logger
from .lib.simadb import SimaDB
from .utils.config import ConfMan
from .utils.startopt import StartOpt
from .utils.utils import exception_log, SigHup
 # core plugins
from .plugins.core.history import History
from .plugins.core.mpdoptions import MpdOptions
##


def load_plugins(sima, source):
    """Handles internal/external plugins
        sima:   sima.core.Sima instance
        source: ['internal', 'contrib']
    """
    if not sima.config.get('sima', source):
        return
    logger = logging.getLogger('sima')
    for plugin in sima.config.get('sima', source).split(','):
        plugin = plugin.strip(' \n')
        module = 'sima.plugins.{0}.{1}'.format(source, plugin.lower())
        try:
            mod_obj = __import__(module, fromlist=[plugin])
        except ImportError as err:
            logger.error('Failed to load plugin\'s module: ' +
                         '{0} ({1})'.format(module, err))
            sima.shutdown()
            sys.exit(1)
        try:
            plugin_obj = getattr(mod_obj, plugin)
        except AttributeError as err:
            logger.error('Failed to load plugin {0} ({1})'.format(plugin, err))
            sima.shutdown()
            sys.exit(1)
        logger.info('Loading {0} plugin: {name} ({doc})'.format(
                             source, **plugin_obj.info()))
        sima.register_plugin(plugin_obj)


def start(sopt, restart=False):
    """starts application
    """
    # set logger
    verbosity = sopt.options.get('verbosity', 'warning')
    logfile = sopt.options.get('logfile', None)
    set_logger(verbosity, logfile)
    # loads configuration
    config = ConfMan(sopt.options).config
    logfile = config.get('log', 'logfile')
    verbosity = config.get('log', 'verbosity')
    set_logger(verbosity, logfile)
    logger = logging.getLogger('sima')
    logger.debug('Command line say: {0}'.format(sopt.options))
    # Create Database
    db_file = config.get('sima', 'db_file')
    if (sopt.options.get('create_db', None)
       or not isfile(db_file)):
        logger.info('Creating database in "{}"'.format(db_file))
        open(db_file, 'a').close()
        SimaDB(db_path=db_file).create_db()
        if sopt.options.get('create_db', None):
            logger.info('Done, bye...')
            sys.exit(0)

    logger.info('Starting...')
    sima = core.Sima(config)

    # required core plugins
    sima.register_plugin(History)
    sima.register_plugin(MpdOptions)

    #  Loading internal plugins
    load_plugins(sima, 'internal')

    #  Loading contrib plugins
    load_plugins(sima, 'contrib')
    # Run as a daemon
    if config.getboolean('daemon', 'daemon'):
        if restart:
            sima.run()
        else:
            logger.info('Daemonize process...')
            sima.start()

    try:
        sima.foreground()
    except KeyboardInterrupt:
        logger.info('Caught KeyboardInterrupt, stopping')
        sys.exit(0)


def run(sopt, restart=False):
    """
    Handles SigHup exception
    Catches Unhandled exception
    """
    # pylint: disable=broad-except
    try:
        start(sopt, restart)
    except SigHup:  # SigHup inherit from Exception
        run(sopt, True)
    except Exception:  # Unhandled exception
        exception_log()

# Script starts here
def main():
    """Entry point"""
    nfo = dict({'version': info.__version__,
                 'prog': 'sima'})
    # StartOpt gathers options from command line call (in StartOpt().options)
    sopt = StartOpt(nfo)
    run(sopt)


if __name__ == '__main__':
    main()

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab
