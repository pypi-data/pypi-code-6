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

import msgpack
from tornado.options import define, options
from tornado.options import parse_command_line

from cocaine.services import Service

log = logging.getLogger()

AppGroup = "Application"
CocaineGroup = "Cocaine"
ActionGroup = "Actions"

POSSIBLE_ACTIONS = ('upload', 'deploy', 'start', 'stop')


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
    if options.action not in POSSIBLE_ACTIONS:
        log.error("Option 'action' must be one of %s",
                  ', '.join(POSSIBLE_ACTIONS))
        options.print_help()
        exit(1)


@Dispatcher.attach("upload")
def upload():
    task = {"appname": options.appname,
            "version": options.version,
            "url": options.url}

    s = Service("flow@main", host=options.host, port=options.port)
    try:
        map(log.info, s.enqueue("upload", msgpack.packb(task)))
    except Exception as err:
        log.error(err)
        exit(1)


@Dispatcher.attach("start")
def start():
    task = {"appname": options.appname}
    if options.profile:
        task["profilename"] = options.profile

    s = Service("flow@main", host=options.host, port=options.port)
    try:
        map(log.info, s.enqueue("start", msgpack.packb(task)))
    except Exception as err:
        log.error(err)
        exit(1)


@Dispatcher.attach("stop")
def stop():
    task = {"appname": options.appname}

    s = Service("flow@main", host=options.host, port=options.port)
    try:
        map(log.info, s.enqueue("stop", msgpack.packb(task)))
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

    s = Service("flow@main", host=options.host, port=options.port)
    try:
        map(log.info, s.enqueue("deploy", msgpack.packb(task)))
    except Exception as err:
        log.error(err.msg)
        exit(1)


def main():
    options.add_parse_callback(check_options)
    parse_command_line()
    Dispatcher.run(options.action)


if __name__ == '__main__':
    main()
