import os
import time
import socket
import RPi.GPIO as GPIO
import pykka

from mopidy import core

class GPIOFrontEnd(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(GPIOFrontEnd, self).__init__()
        self.core = core

