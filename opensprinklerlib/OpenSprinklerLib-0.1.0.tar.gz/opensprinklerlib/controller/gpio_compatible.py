#!/usr/bin/env python

try:
    # Attempt to load RPi Module
    import RPi.GPIO as GPIO
except:
    try:
        # Attempt to load Beagle Bone Module
        import Adafruit_BBIO.GPIO as GPIO
    except:
        pass

from controller import *


class GPIOCompatible(Controller):
    """GPIO interface compatible Controller abstract class.

    Currently used by the rpi and beagle bone controller classes

    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """GPIO Compatible Class Initializer
        """
        super(GPIOCompatible, self).__init__()

    def __del__(self):
        self._shiftOut()
        GPIO.cleanup()

    def _init_hardware(self):
        self._setup_pins()
        self._init_gpio()

    @abc.abstractmethod
    def _setup_pins(self):
        return

    def _init_gpio(self):
        GPIO.setup(self._pin_sr_clk, GPIO.OUT)
        GPIO.setup(self._pin_sr_noe, GPIO.OUT)
        self._disableShiftRegisterOutput()
        GPIO.setup(self._pin_sr_dat, GPIO.OUT)
        GPIO.setup(self._pin_sr_lat, GPIO.OUT)

        self._shiftOut()
        self._enableShiftRegisterOutput()

    def _enableShiftRegisterOutput(self):
        GPIO.output(self._pin_sr_noe, False)

    def _disableShiftRegisterOutput(self):
        GPIO.output(self._pin_sr_noe, True)

    def _shiftOut(self):
        GPIO.output(self._pin_sr_clk, False)  # need to test to see if this is necessary
        GPIO.output(self._pin_sr_lat, False)
        for s in range(0, self._MAX_NSTATIONS):
            GPIO.output(self._pin_sr_clk, False)
            GPIO.output(self._pin_sr_dat, 1 if (self._station_bits[self._MAX_NSTATIONS-1-s] == 1) else 0)
            GPIO.output(self._pin_sr_clk, True)
        GPIO.output(self._pin_sr_lat, True)

    def enable(self, sid):
        self._station_bits[sid - 1] = 1
        self._shiftOut()

    def disable(self, sid):
        self._station_bits[sid - 1] = 0
        self._shiftOut()
