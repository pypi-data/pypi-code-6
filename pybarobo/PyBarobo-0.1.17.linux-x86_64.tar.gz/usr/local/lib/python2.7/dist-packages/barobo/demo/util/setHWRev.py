#!/usr/bin/env python

from barobo import Linkbot, Dongle
import time
import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print ("Usage: {0} <Com_Port> <major> <minor> <micro>".format(sys.argv[0]))
        quit()
    if len(sys.argv) == 3:
        serialID = sys.argv[2]
    else:
        serialID = None
    dongle = Dongle()
    dongle.connectDongleSFP(sys.argv[1])
    linkbot = dongle.getLinkbot(serialID)

    linkbot.setHWRev(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
