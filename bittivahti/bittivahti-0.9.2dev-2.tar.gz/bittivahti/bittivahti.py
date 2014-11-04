#!/usr/bin/python
# -*- coding: utf-8 -*-

PROGRAM = 'bittivahti'
VERSION = '0.9.2'
DEVFILE = '/proc/net/dev'

import re
import sys
import time

from .utils import clear, pretty_unit

# Python 3 int is long
if sys.version > '3':
    long = int


class Bittivahti:
    device = {}
    delta = {}
    total = {}
    start = time.time()
    period = None

    def updatevalues(self):
        lines = None
        # Read network traffic stats to memory quickly
        with open(DEVFILE, 'r') as f:
            lines = f.readlines()[2:]
            curtime = time.time()
            self.period = curtime - self.start
            self.start = curtime

        for line in lines:
            data = re.split('[ \t:]+', line.strip())
            iface = data[0]
            rx, rxp = map(long, data[1:3])
            tx, txp = map(long, data[9:11])
            trafficdata = [rx, tx, rxp, txp]

            if rx > 0 or tx > 0:
                if iface in self.device:
                    self.delta[iface] = [b-a for a, b in zip(self.device[iface], trafficdata)]
                else:
                    self.delta[iface] = [long(0)]*4
                    self.total[iface] = [long(0)]*4
                self.device[iface] = trafficdata

                # Calculate self.total amount of traffic
                if True in [a < 0 for a in self.delta[iface]]:
                    pass  # ignore updates where bytes or packets is negative
                else:
                    self.total[iface] = [a+b for a, b in zip(self.total[iface], self.delta[iface])]

    def printdata(self):
        print(PROGRAM, VERSION)
        print("interface   |      RX bw / packets |      TX bw / packets | "
              "self.total:  RX       TX ")

        for iface in self.device.keys():
            rx, tx, rxp, txp = [x/self.period for x in self.delta[iface]]
            rx_t, tx_t, rxp_t, txp_t = self.total[iface]
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

    def loop(self, sleep, dynunit, colours):
        print('Please wait. The display is updated every {sleep:.0f} seconds.'
              .format(sleep=sleep))
        print('Starting up...')
        self.updatevalues()
        time.sleep(sleep)
        # Main loop
        while True:
            try:
                clear()
                self.updatevalues()
                self.printdata()
                time.sleep(sleep)
            except KeyboardInterrupt:
                raise SystemExit('\n\nBye!')
