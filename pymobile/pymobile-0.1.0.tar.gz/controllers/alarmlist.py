#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import bottle
from pymobile import shared, wsfunc
import asyncio
import json

from models import alarmlist_example as alarmlist

@bottle.route('/alarmlist')
@bottle.route('/alarmlist/')
@bottle.view('alarmlist')
def webalarmlist():
    ''' Lister opp alle pc-er '''
    user = shared.session['user']
    if not user:
       bottle.abort(401)
    else:
        alarms = alarmlist.getAlarms()
        #print(alarms)
        return dict(user=user, alarms=alarms)


def get_alarmlist_diff(alarmqueue):
    return alarmqueue.get() # blocking. wait for new alarmdata

@wsfunc.add
def update_alarmlist(ws, uri):
    loop = asyncio.get_event_loop()
    alarmqueue = alarmlist.get_alarmqueue()
    while ws.open:
        alarmdata = yield from loop.run_in_executor(None, get_alarmlist_diff, alarmqueue)
        if ws.open and alarmdata:
            yield from ws.send(json.dumps(alarmdata))
        #yield from asyncio.sleep(0.1)
    alarmlist.remove_alarmqueue(alarmqueue)

@wsfunc.add
@asyncio.coroutine
def ack_alarm(ws, uri, dpe):
    alarmlist.ack_alarm(dpe)