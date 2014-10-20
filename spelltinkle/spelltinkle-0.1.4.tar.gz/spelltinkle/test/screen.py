import os
import signal
import locale
import termios
import threading
import tty
import sys
from time import time

from logging import debug


class Screen:
    def __init__(self, size=None, corner=(0, 0)):
        self.size = size
        self.w, self.h = size
            
    def write(self, text=' ', colors=0):
        if isinstance(colors, int):
            colors = [colors] * len(text)
        c0 = None
        for x, color in zip(text, colors):
            if color != c0:
                print(self.colors[color], end='')
                c0 = color
            print(x, end='')

    def move(self, y, x):
        print('\x1b[{};{}H'.format(y + 1 + self.corner[1], x + 1), end='')
        self.c = x
