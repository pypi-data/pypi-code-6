#!/usr/bin/env python3
from threading import Thread
import asyncio
import websockets
import json
import logging
import pickle
import base64
#import ssl
from pymobile import shared

# dict of functions exposed to websocket
funcDict = dict()
host = 'localhost'
port = 8765


# use this decorator to expose function to websockets
def add(func):
    funcDict[func.__name__] = func


# helperfunction to call exposed function
def call(ws, uri, method, args=[], kwargs={}):
    return funcDict[method](ws, uri, *args, **kwargs)


def userPermission(ws):
    for cookies in ws.raw_request_headers:
        if cookies[0] == 'Cookie':
            for cookie in cookies[1].split('; '):
                if cookie.startswith('pym-sid='):
                    sid = pickle.loads(base64.b64decode(cookie.split('?')[1]))[1]
                    return shared.session.get_from(sid, 'user',False)
    return False


# test of the 'add' decorator
@add
def test(ws, uri, *arg, **kwargs):
    while ws.open:
        logging.info('jazz')
        yield from ws.send('jazz')
        yield from asyncio.sleep(5)


@asyncio.coroutine
def onmessage(ws, uri):
    """ This function is called when websocket receive a message.
        The message is parsed with jquery and expect following data format:
        [(str)method, (list)arguments, (dict)keyword arguments]
        if this function exists it will be called and result is yield back
    """
    if userPermission(ws):
        loop = asyncio.get_event_loop()
        while ws.open:
            encoded_data = yield from ws.recv()
            if encoded_data is None:
                break
            data_object = json.loads(encoded_data)
            logging.info('received: {!r}'.format(data_object))
            method, args, kwargs = data_object
            try:
                asyncio.async(call(ws, uri, method, args, kwargs))
            except KeyError:
                logging.error("Websocket method {} not defined in server".format(method))
            
        logging.info('ok close')
    else:
        logging.info('auth error. close')

def livecounter(loop):
    # prevent blocking
    loop.call_later(0.2, livecounter, loop)
    
    
class WSServer(Thread):
    def __init__(self):
        super().__init__(name='Websocket')
        self.loop = None
        self.server = None
        self.host = host
        self.port = port

    def run(self):
        """Run the websocket server"""
        #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        #ssl_context.load_cert_chain(certfile='cert.crt', keyfile='cert.key')
        #ssl_context.verify_mode = ssl.CERT_NONE
        for func in funcDict.keys():
            logging.info('adding function {} to websockets'.format(func))

        logging.info('Websocket listening on http://{}:{}/'.format(self.host, self.port))
        self.server = websockets.serve(onmessage, self.host, self.port)#, ssl=ssl_context)
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.server)
        self.loop.call_soon(livecounter, self.loop)
        self.loop.run_forever()
        logging.info('Websocket event loop stopped')

    def stop(self):
        if self.loop:
            self.loop.stop()
        if self.server:
            self.server.close()


class WS(object):
    def __init__(self):
        self.sock = WSServer()
        self.sock.start()

    def __del__(self):
        self.sock.stop()
        self.sock.join()

def run_in_thread():
    # in blender:
    return WS()


server = None


def start():
    global server
    server = run_in_thread()


def stop():
    global server
    server = None


def run():
    # everywhere else:
    try:
        print('go')
        WSServer().run()
    except KeyboardInterrupt:
        print('fin')

if __name__ == '__main__':
    run()