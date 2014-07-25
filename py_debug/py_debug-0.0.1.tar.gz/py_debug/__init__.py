# coding: utf-8

import os
import re
import sys
import time
import logging
from random import randint

reg = None
enabled = False
colors = [
    '31',
    '32',
    '33',
    '34',
    '35',
    '36'
]

def init():
    env = os.environ.get('DEBUG')

    if env is not None:
        enable(env)

def enable(pattern):
    global reg, enabled
    pattern = re.escape(pattern)
    pattern = re.sub(r'\\\*', '.*?', pattern)
    pattern = re.sub(',', '|', pattern)
    pattern = '^(' + pattern + ')$'
    reg = re.compile(pattern)
    enabled = True

def disable():
    global enabled
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

init()
