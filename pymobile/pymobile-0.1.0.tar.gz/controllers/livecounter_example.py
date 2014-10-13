#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymobile import shared, wsfunc
import asyncio
import json
import threading

# syncronize between two threads.
ready = threading.Event()

@shared.worker
def livecounter_worker():
    shared.state['livecounter'] = 0
    
    while not shared.stop.wait(0.3):
        with shared.lock:
            shared.state['livecounter'] += 1
            ready.set()
    ready.set()


# blocking function called from asyncio with executor.
def livecounter_changed():
    ready.wait()
    ready.clear()
    return shared.state['livecounter']
        
@wsfunc.add
def livecounter(ws, uri):
    loop = asyncio.get_event_loop()
    while ws.open:
        future = loop.run_in_executor(None, livecounter_changed)
        res = yield from future
        if ws.open:
            data = json.dumps(res)
            yield from ws.send(data)
            yield from asyncio.sleep(0.1)
            #ready.clear()
