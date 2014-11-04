#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import time

program = 'bittivahti'
version = '0.9.2'

devfile = '/proc/net/dev'

device = {}
delta = {}
total = {}
start = time.time()
period = None


def pretty_unit(value, base=1000, minunit=None, format="%0.1f"):
    '''Finds the correct unit and returns a pretty string

    pretty_unit(4190591051, base=1024) = "3.9 Gi"
    '''
    if not minunit:
        minunit = base

    # Units based on base
    if base == 1000:
        units = [' ', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    elif base == 1024:
        units = ['  ', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi']
    else:
        raise ValueError("The unit base has to be 1000 or 1024")

    # Divide until below threshold or base
    v = float(value)
    u = base
    for unit in units:
        if v >= base or u <= minunit:
            v = v/base
            u = u * base
        else:
            if v >= 10:
                return "%0.0f %s" % (v, unit)
            else:
                return format % v + units[0] + unit


def updatevalues():
    global start, period
    lines = None
    # Read network traffic stats to memory quickly
    with open(devfile, 'r') as f:
        lines = f.readlines()[2:]
        curtime = time.time()
        period = curtime - start
        start = curtime

    for line in lines:
        data = re.split('[ \t:]+', line.strip())
        iface = data[0]
        rx, rxp = map(long, data[1:3])
        tx, txp = map(long, data[9:11])
        trafficdata = [rx, tx, rxp, txp]

        if rx > 0 or tx > 0:
            if iface in device:
                delta[iface] = [b-a for a, b in zip(device[iface], trafficdata)]
            else:
                delta[iface] = [0L, 0L, 0L, 0L]
                total[iface] = [0L, 0L, 0L, 0L]
            device[iface] = trafficdata

            # Calculate total amount of traffic
            if True in [a < 0 for a in delta[iface]]:
                pass  # ignore updates where bytes or packets is negative
            else:
                total[iface] = [a+b for a, b in zip(total[iface], delta[iface])]


def printdata():
    print program, version
    print "interface   |      RX bw / packets |      TX bw / packets | " + \
        "total:  RX       TX "

    for iface in device.keys():
        rx, tx, rxp, txp = map(lambda x: x/period, delta[iface])
        rx_t, tx_t, rxp_t, txp_t = total[iface]
        d = {'iface': iface,
             'rx': pretty_unit(rx),
             'tx': pretty_unit(tx),
             'rxp': pretty_unit(rxp, minunit=1, format="%0.0f"),
             'txp': pretty_unit(txp, minunit=1, format="%0.0f"),
             'rx_t': pretty_unit(rx_t),
             'tx_t': pretty_unit(tx_t)
             }
        print(("%(iface)-12s| %(rx)7sB/s %(rxp)6sp/s |"
               " %(tx)7sB/s %(txp)6sp/s |"
               "   %(rx_t)7sB %(tx_t)7sB") % d)


def clear():
    sys.stdout.write("\x1b[H\x1b[2J")


def loop(sleep, dynunit, colours):
    print 'Please wait. The display is updated every %.0f seconds.' % sleep
    print 'Starting up...'
    updatevalues()
    time.sleep(sleep)
    # Main loop
    while True:
        try:
            clear()
            updatevalues()
            printdata()
            time.sleep(sleep)
        except KeyboardInterrupt:
            print '\n\nBye!'
            sys.exit()
