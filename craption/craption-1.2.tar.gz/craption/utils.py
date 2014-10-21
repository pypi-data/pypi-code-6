#coding: utf-8

import craption.settings
import datetime
import os
import pkg_resources
import pyperclip
import random
import re
import subprocess
import sys
import tempfile
import time

def set_clipboard(data):
    pyperclip.copy(data)

def screenshot():
    path = tempfile.mktemp('.png')
    if sys.platform.startswith('linux'):
        run(['scrot', '-s', path])
    else:
        run(['screencapture', '-ix', path])
    return path

def get_filename():
    conf = craption.settings.get_conf()
    filename = conf['file']['name']
    now = time.time()
    for match in re.finditer("{r(\d+)}", filename):
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        random_string = "".join([random.choice(chars) for _ in range(int(match.group(1)))])
        filename = filename.replace(match.group(0), random_string)

    filename = filename.replace('{u}', str(int(now)))
    filename = filename.replace('{d}', datetime.datetime.fromtimestamp(now).strftime(conf['file']['datetime_format']))

    return filename + ".png"

def play_noise():
    if sys.platform.startswith('linux'):
        run(["mplayer", craption.settings.noise_path])
    else:
        run(["afplay", craption.settings.noise_path])

def install():
    with open(craption.settings.noise_path, 'wb') as fh:
        fh.write(pkg_resources.resource_stream('craption', 'noise.wav').read())
    craption.settings.write_template()
    exit(0)

def run(args):
    devnull = open(os.devnull, 'wb')
    p = subprocess.Popen(args, stdout=devnull, stderr=devnull)
    p.wait()
