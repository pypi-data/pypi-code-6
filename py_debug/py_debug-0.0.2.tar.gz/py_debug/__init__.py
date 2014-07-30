# coding: utf-8

import os
import re
import sys
import time
import socket
import logging
from random import randint
from threading import Thread, Lock

reg = None
enabled = False
writer = None
socketThread = None
lock = Lock()
colors = [
    '31',
    '32',
    '33',
    '34',
    '35',
    '36'
]

def init():
    global socketThread

    env = os.environ.get('DEBUG')

    if env is not None:
        enable(env)
    
    socketThread = Thread(target=serve)
    socketThread.setDaemon(True)
    socketThread.start()

def enable(pattern):
    global reg, enabled
    pattern = re.escape(pattern)
    pattern = re.sub(r'\\\*', '.*?', pattern)
    pattern = re.sub(',', '|', pattern)
    pattern = '^(' + pattern + ')$'
    with lock:
        reg = re.compile(pattern)
        enabled = True

def disable():
    global enabled
    with lock:
        enabled = False

def debug(name):
    context = {}
    context['name'] = name;
    context['color'] = randColor()
    context['logger'] = createLogger(name, context['color'])
    context['prevTime'] = time.time()

    def debugFunction(message, context):
        if not enabled or reg.match(context['name']) is None:
            return

        delta = getDelta(context['prevTime'], context['color'])
        message = delta + ' ' + message

        if writer is not None:
            socketMessage = '\033[' + context['color'] + 'm' + context['name'] + '\033[0m '
            socketMessage += message + '\n'
            writer.send(socketMessage)

        context['logger'].debug(message);
        context['prevTime'] = time.time()

    return lambda message: debugFunction(message, context)

def createLogger(name, color):
    logger = logging.getLogger(name)
    
    fmt = '%(asctime)s %(name)s %(message)s'

    if sys.stdout.isatty():
        fmt = '  \033[' + color + 'm%(name)s\033[0m %(message)s'

    formatter = logging.Formatter(fmt);

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)

    return logger

def randColor():
    n = randint(0, len(colors) - 1)
    return colors[n]

def getDelta(prevTime, color):
    now = time.time()
    delta = (now - prevTime) * 1000000000
    delta = humanizeNano(delta)
    return '\033[' + color + 'm+' + delta + '\033[0m'

def humanizeNano(n):
    suffix = 'ns'
    
    if n > 1e9:
        n /= 1e9
        suffix = 's'
    elif n > 1e6:
        n /= 1e6
        suffix = 'ms'
    elif n > 1e3:
        n /= 1e3
        suffix = 'us'

    return str(int(n)) + suffix

# temporary unix domain socket
def serve():
    path = '/tmp/debug-%s.sock' % os.getpid()

    # Make sure the socket does not already exist
    try:
        os.unlink(path)
    except OSError:
        if os.path.exists(path):
            print 'The socket %s does already exists' % path
            raise

    # create socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(path)
    sock.listen(1)
    talk(sock)

# TODO: support multiple listeners
def talk(sock):
    global writer

    while True:
        conn, client_address = sock.accept()
        try:
            with lock:
                writer = conn
            while True:
                cmd = conn.recv(16)
                if not recv(cmd)(conn):
                    break
        finally:
            conn.close()

def recv(cmd):
    cmd = cmd.strip(' \t\n\r')

    def quitHandler(conn):
        print 'debug: quit'
        disable()
        conn.close()
        return False

    def disableHandler(conn):
        print 'debug: disabling'
        disable()
        return True

    def defaultHandler(conn):
        print 'debug: enabling %s' % cmd
        enable(cmd)
        return True

    handler = None

    try:
        handler = {
            'q': quitHandler,
            'quit': quitHandler,
            'd': disableHandler,
            'disable': disableHandler
        }[cmd]
    except:
        handler = defaultHandler

    return handler

init()
