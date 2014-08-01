# -*- coding: utf-8 -*-
#
# Copyright © 2014, Emutex Ltd.
# All rights reserved.
# http://www.emutex.com
#
# Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>
#
# See license in LICENSE.txt file.
#
# This example is inspired on Arduino Fade example.
# http://arduino.cc/en/Tutorial/Fade


# Import the GPIOGalileoGen2 class from the wiringx86 module.
from wiringx86 import GPIOGalileoGen2 as GPIO
import time

# Create a new instance of the GPIOGalileoGen2 class.
# Setting debug=True gives information about the interaction with sysfs.
gpio = GPIO(debug=False)
brightness = 0
fadeAmount = 5
pins = (3, 5, 6, 9, 10, 11)
periods = (1000000, 2000000, 3000000, 4000000, 5000000, 6000000)
# Set all pins to be used as output GPIO pins.
print 'Setting up all pins...'

for pin, period in zip(pins, periods):
    print '%d -> %d' % (pin, period)
    gpio.pinMode(pin, gpio.PWM)
    gpio.setPWMPeriod(pin, period)

print 'Fading all pins now...'
try:
    while(True):
        # Write brightness to the pin. The value must be between 0 and 255.
        for pin in pins:
            gpio.analogWrite(pin, brightness)

        # Increment or decrement the brightness.
        brightness = brightness + fadeAmount

        # If the brightness has reached its maximum or minimum value swap
        # fadeAmount sign so we can start fading the led on the other direction.
        if brightness == 0 or brightness == 255:
            fadeAmount = -fadeAmount

        time.sleep(0.01)

# When you get tired of seeing the led fading kill the loop with Ctrl-C.
except KeyboardInterrupt:
    # Leave the led turned off.
    print '\nCleaning up...'
    for pin in pins:
        gpio.analogWrite(pin, 0)

    # Do a general cleanup. Calling this function is not mandatory.
    gpio.cleanup()
