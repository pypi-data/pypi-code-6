#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""This module contains command line endpoints to run the program from shell
"""

import os
import sys
import argparse

import drove
import drove.log
import drove.daemon
import drove.config
import drove.plugin
import drove.channel
import drove.reloader

from drove.util.network import getfqdn


def cli():
    """Base command line executable.
    """

    cmdopt = argparse.ArgumentParser(
        description="%s %s: %s" % (drove.NAME, drove.VERSION,
                                   drove.DESCRIPTION,))

    cmdopt.add_argument("-C", "--config-file", action="store",
                        dest="config_file",
                        help="Main configuration file to read.",
                        type=str,
                        default=None)

    cmdopt.add_argument("-v", "--verbose", action="store_true",
                        dest="verbose",
                        help="be verbose",
                        default=False)

    cmdopt.add_argument("-s", "--set", action="append",
                        dest="set",
                        help="set config variables by hand (key=value). " +
                             "This option will override values from " +
                             "config file.",
                        default=[])

    cmdopt.add_argument('-V', '--version', action='version',
                        version="%(prog)s " + drove.VERSION)

    cmdopt.add_argument('-f', '--foreground', action='store_true',
                        dest="foreground",
                        help="No daemonize and run in foreground.",
                        default=False)

    args = cmdopt.parse_args()

    # read configuration and start reload timer.
    if args.config_file:
        config = drove.config.Config(args.config_file)
    else:
        cf = os.path.expanduser("~/.config/drove/drove.conf")
        uf = os.path.expanduser("~/.drove/drove.conf")
        gf = "/etc/drove/drove.conf"
        dc = os.path.join(os.path.dirname(__file__), "config", "drove.conf")
        if os.path.isfile(cf):
            config = drove.config.Config(cf)
        elif os.path.isfile(uf):
            config = drove.config.Config(uf)
        elif os.path.isfile(gf):
            config = drove.config.Config(gf)
        elif os.path.isfile(dc):
            config = drove.config.Config(dc)
        else:
            config = drove.config.Config()

    if args.set:
        for config_val in args.set:
            if "=" not in config_val:
                raise ValueError("--set option requires a " +
                                 "'key=value' argument.")
            key, val = config_val.split("=", 1)
            config[key] = val

    # ensure that config has nodename or create nodename for this node
    if config.get("nodename", None) is None:
        config["nodename"] = getfqdn

    # configure log, which is a singleton, no need to use parameters
    # in log in any other places.
    log = drove.log.getLogger(syslog=config.get("syslog", True),
                              console=config.get("logconsole", False),
                              logfile=config.get("logfile", None),
                              logfile_size=config.get("logfile_size", 0),
                              logfile_keep=config.get("logfile_keep", 0))
    if args.verbose:
        log.setLevel(drove.log.DEBUG)

    try:
        from setproctitle import setproctitle
        setproctitle("drove %s" % " ".join(sys.argv[1:]))
    except ImportError:
        pass

    log.info("Starting drove")

    # create a common channel to communicate the plugins
    log.debug("Creating channel")
    channel = drove.channel.Channel()

    # starting plugins
    log.debug("Starting plugins")
    plugins = drove.plugin.PluginManager(config, channel)

    if len(plugins) == 0:
        log.warning("No plugins installed... " +
                    "drove has no work to do.")

    def _exit_handler(*args, **kwargs):
        log.error("Received TERM signal. Try to exit gently...")
        plugins.stop_all()
        sys.exit(15)

    def _daemon():
        try:
            plugins.start_all()

            # starting reload thread
            log.debug("Starting reloader")
            reloader = drove.reloader.Reloader([getfqdn, config] +
                                               [x for x in plugins],
                                               interval=config.get(
                                                   "reload",
                                                   60))
            reloader.start()

            # wait until all plugins stop
            log.info("Entering data gathering loop")
            plugins.loop()

        except KeyboardInterrupt:
            log.fatal("Received a Keyboard Interrupt. Exit silently.")
            sys.exit(15)
        except BaseException as e:
            if args.verbose:
                raise
            log.fatal("Unexpected error happened during drove execution: " +
                      "{message}".format(message=str(e)))
            sys.exit(1)

    # setup daemon, but not necessary run in background
    daemon = drove.daemon.Daemon.create(_daemon, _exit_handler)  # handle TERM
    if args.foreground:
        # starting daemon in foreground if flag is preset
        daemon.foreground()
    else:
        # or start it as daemon
        daemon.start()


if __name__ == "__main__":
    cli()
