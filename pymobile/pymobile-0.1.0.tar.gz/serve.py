#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from importlib import import_module
import bottle
from pymobile import shared
import logging
import settings
from pymobile import wsfunc

# setup logging
logging.basicConfig(
    format='%(asctime)-15s %(levelname)-9s: %(threadName)-11s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG if settings.debug else logging.INFO)

# get a list of all modules in controller-folder
controllers = os.listdir('controllers')
controllers.sort()

# import all modules from controllers-folder
for c in controllers:
    if not c.startswith('__') and c.endswith('.py'):
        logging.info('importing {} from controllers'.format(c))
        import_module('controllers.{}'.format(c[:-3]))

# enable shared session
shared.session._sid = lambda:bottle.request.get_cookie(
    'pym-sid',
    secret=settings.secret_key)

shared.session._registersid = lambda sid:bottle.response.set_cookie(
    'pym-sid',
    sid,
    secret=settings.secret_key,
    max_age=settings.max_age)


def run(host=settings.host, port=settings.port, reloader=False):
    try:
        # start all shared workers
        shared.workers.start()

        # start websocket-server
        wsfunc.host = settings.ws_host
        wsfunc.port = settings.ws_port
        wsfunc.start()

        # start web-interface and block until ctrl-c
        bottle.DEBUG=settings.debug
        bottle.run(host=host, port=port, reloader=reloader)
        
    finally:
        # stop all shared workers
        shared.workers.stop()

        # stop websocket-server
        wsfunc.stop()

if __name__ == '__main__':
    run()

