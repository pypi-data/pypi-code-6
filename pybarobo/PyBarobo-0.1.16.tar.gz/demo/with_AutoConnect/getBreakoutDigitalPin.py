#!/usr/bin/env python

from barobo import Linkbot, Dongle
import barobo
import time
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: {0} [Linkbot Serial ID]".format(sys.argv[0]))
        quit()
    serialID = sys.argv[1]
    dongle = Dongle()
    dongle.connect()
    linkbot = dongle.getLinkbot(serialID)

    # Set all pins to input
    map( lambda pin: linkbot.setBreakoutPinMode(pin, barobo.PINMODE_INPUT), 
            range(2,14))

    print (list(map(linkbot.getBreakoutDigitalPin, range(2, 14))))
