#!/usr/bin/env python
# encoding: utf-8
#
#    Copyright (c) 2013-2014+ Anton Tyurin <noxiouz@yandex.ru>
#    Copyright (c) 2013-2014 Other contributors as noted in the AUTHORS file.
#
#    This file is part of Cocaine.
#
#    Cocaine is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Cocaine is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function

import logging
import os
import sys

import msgpack
from tornado.options import define, options
from tornado.options import parse_command_line, parse_config_file

from cocaine.services import Service

log = logging.getLogger()

AppGroup = "Application"
CocaineGroup = "Cocaine"
ActionGroup = "Actions"

POSSIBLE_ACTIONS = ('upload', 'deploy', 'start', 'stop', 'listing', 'undeploy')
API_VERSION = 1.1


class Dispatcher(object):
    dispatch_tree = {}

    @classmethod
    def attach(cls, action_name):
        def wrapper(func):
            cls.dispatch_tree[action_name] = func
            return func
        return wrapper

    @classmethod
    def run(cls, action):
        return cls.dispatch_tree[action]()


class Printer(object):
    def __init__(self, print_func=None):
        self._prev = ''
        if print_func is not None:
            self._print_func = print_func

    def _print_func(self, value):
        print(value.strip('\n'))

    def log(self, value):
        if value != self._prev:
            self._prev = str(value)
            self._print_func(self._prev)

# AppGroup
define('appname', group=AppGroup,
       help='application name',
       type=str, default=None),

define('version', group=AppGroup,
       help='version',
       type=str, default=None)

define('url', group=AppGroup,
       help='repository url',
       type=str, default=None)

define('profile', group=AppGroup,
       help='profile to deploy with',
       type=str, default=None)

define('weight', group=AppGroup,
       help='application weight in group',
       type=int, default=0)

define('username', group=CocaineGroup,
       help='username',
       type=str)

# CocaineGroup
define('host', group=CocaineGroup,
       help='Host of buildfarm locator',
       type=str, default="localhost")

define('port', group=CocaineGroup,
       help='Port of buildfarm locator',
       type=int, default=10053)

# ActionGroup
define('action', group=ActionGroup,
       help='action name (upload|deploy|start|stop)',
       type=str, default=None)


def check_options():
    try:
        if options.action not in POSSIBLE_ACTIONS:
            log.error("Option 'action' must be one of %s",
                      ', '.join(POSSIBLE_ACTIONS))
            raise Exception()
        if options.username is None:
            log.error("Specify username by --username option")
            raise Exception()
    except Exception:
        options.print_help()
        exit(1)


def gen_task(task):
    return msgpack.packb({"task": task,
                          "API": API_VERSION,
                          "username": options.username})


@Dispatcher.attach("upload")
def upload():
    task = {"appname": options.appname,
            "version": options.version,
            "url": options.url}

    try:
        s = Service("flow@main", host=options.host, port=options.port)
        printer = Printer()
        map(printer.log, s.enqueue("upload",
                                   gen_task(task)))
    except Exception as err:
        log.error(err)
        exit(1)


@Dispatcher.attach("start")
def start():
    task = {"appname": options.appname,
            "version": options.version}
    if options.profile:
        task["profilename"] = options.profile

    try:
        s = Service("flow@main", host=options.host, port=options.port)
        printer = Printer()
        map(printer.log, s.enqueue("start", gen_task(task)))
    except Exception as err:
        log.error(err)
        exit(1)


@Dispatcher.attach("stop")
def stop():
    task = {"appname": options.appname,
            "version": options.version}

    try:
        s = Service("flow@main", host=options.host, port=options.port)
        printer = Printer()
        map(printer.log, s.enqueue("stop", gen_task(task)))
    except Exception as err:
        log.error(err)
        exit(1)


@Dispatcher.attach("deploy")
def deploy():
    log.info("Application %s would be deployed with profile %s."
             " Its weight would be %d",
             options.appname,
             options.profile, options.weight)
    task = {"appname": options.appname,
            "version": options.version,
            "profilename": options.profile,
            "weight": options.weight}

    try:
        s = Service("flow@main", host=options.host, port=options.port)
        printer = Printer()
        map(printer.log, s.enqueue("deploy", gen_task(task)))
    except Exception as err:
        log.error(err.msg)
        exit(1)


@Dispatcher.attach("undeploy")
def undeploy():
    log.info("Application %s would be undeployed with profile.",
             options.appname)
    task = {"appname": options.appname,
            "version": options.version}

    try:
        s = Service("flow@main", host=options.host, port=options.port)
        printer = Printer()
        map(printer.log, s.enqueue("undeploy", gen_task(task)))
    except Exception as err:
        log.error(err.msg)
        exit(1)


@Dispatcher.attach("listing")
def listing():
    log.info("Fetching a list of your applications")
    try:
        s = Service("flow@main", host=options.host, port=options.port)
        apps = s.enqueue("list",
                         gen_task(None)).get()
        print("User\t\t\tApplication\t\t\tVersion")
        for app, version in (item.rsplit('_', 1) for item in apps):
            user, appname = app.split('_', 1)
            print(user, '\t\t', app, '\t\t', version)
    except Exception as err:
        log.error(err)
        exit(1)


def main():
    HOME_CONFIG_PATH = os.path.expanduser("~/.cocaine.conf")
    if os.path.exists(".cocaine.conf"):
        CONFIG_PATH = ".cocaine.conf"
    else:
        CONFIG_PATH = HOME_CONFIG_PATH

    try:
        if os.path.exists(CONFIG_PATH):
            parse_config_file(CONFIG_PATH, final=False)
        options.add_parse_callback(check_options)
        parse_command_line()
    except Exception as err:
        print("unable to parse options: %s" % err, file=sys.stderr)
        exit(1)
    log.info("user `%s` is working with cloud at %s:%d",
             options.username, options.host, options.port)
    Dispatcher.run(options.action)


if __name__ == '__main__':
    main()
