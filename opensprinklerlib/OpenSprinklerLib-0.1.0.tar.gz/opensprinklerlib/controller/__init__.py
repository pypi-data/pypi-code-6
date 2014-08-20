#!/usr/bin/env python
"""Controller class that auto detects the platform
returning the appropriate class as controller
"""
from .controller import Controller

try:
    # Attempt to load RPi Module
    import RPi.GPIO as GPIO
    from .rpi import rpi as Controller
except:
    try:
        # Attempt to load Beagle Bone Module
        import Adafruit_BBIO.GPIO as GPIO
        from .bb import bb as Controller
    except:
        # Fall back to Mock Controller
        from .mock import mock as Controller
