#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
from gpio_compatible import *


class bb(GPIOCompatible):
    """Beagle Bone Controller class.

    """

    def _init_hardware(self):
        super(bb, self)._init_hardware()
        self._platform = "bb"

    def _setup_pins(self):
        # Beagle Bone PIN DEFINES
        self._pin_sr_clk = "P9_13"
        self._pin_sr_noe = "P9_14"
        self._pin_sr_dat = "P9_11"
        self._pin_sr_lat = "P9_12"
