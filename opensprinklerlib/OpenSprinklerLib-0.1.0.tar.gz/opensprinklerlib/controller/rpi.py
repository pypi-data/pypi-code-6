#!/usr/bin/env python

import RPi.GPIO as GPIO
from gpio_compatible import *


class rpi(GPIOCompatible):
    """Rpi Controller class.

    """

    def _init_hardware(self):
        super(rpi, self)._init_hardware()
        self._platform = "rpi"

    def _setup_pins(self):
        # OSPI PIN DEFINES
        GPIO.setmode(GPIO.BOARD)
        self._pin_sr_clk = 7
        self._pin_sr_noe = 11
        self._pin_sr_dat = 13
        self._pin_sr_lat = 15
