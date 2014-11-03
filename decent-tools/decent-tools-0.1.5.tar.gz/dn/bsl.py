#!/usr/bin/env python

import msp430.bsl.target as bsl
from msp430 import memory
import ftdicbus

import logging
import time
import sys
import argparse

logger = logging.getLogger(__name__)

class DnBsl(bsl.SerialBSLTarget):

    def reset(self):
        """Reset the device."""
        
        self.logger.info('Reset device')
        
        self.set_RST(True)
        self.set_TEST(True)
        time.sleep(0.1)
        
        self.set_RST(False)
        time.sleep(0.1)
        self.set_RST(True)
        time.sleep(0.1)

    def add_dn_options(self, port, filename):
        self.options, _ = self.parser.parse_args([])
        self.options.invert_test = True
        self.options.invert_reset = True
        self.options.input_format = 'ihex'
        self.options.speed = 38400

        self.options.do_mass_erase = True
        self.add_action(self.mass_erase)

        self.options.do_program = True
        self.add_action(self.program_file)
        
        self.download_data = memory.Memory()
        data = memory.load(filename, format=self.options.input_format)
        self.download_data.merge(data)
        
        self.options.port = port

        self.options.do_reset = True
        self.add_action(self.reset)

        segs = [len(seg) + 1 if len(seg) & 1 else len(seg) for seg in self.download_data]
        self.total = sum(segs)
        self.current = 0

    def memory_write(self, address, data):
        """\
        Write to memory. It creates multiple BSL_TXBLK commands internally
        when the size is larger than the block size.
        """
        if len(data) & 1:
            data += '\xff'
            #~ self.log.warn('memory_write: Odd length data not supported, padded with 0xff')
        while data:
            block, data = data[:self.MAXSIZE], data[self.MAXSIZE:]
            if self.extended_address_mode:
                # XXX optimize: send only when offset has changed since previous call
                self.BSL_SETMEMOFFSET(address >> 16)
            self.BSL_TXBLK(address & 0xffff, bytes(block))
            address += len(block)
            self.current += len(block)
            if self.verbose:
                sys.stderr.write("\r Transferred {} of {} bytes ".format(self.current, self.total))

def main():
    parser = argparse.ArgumentParser()
    dbg_grp = parser.add_mutually_exclusive_group()
    dbg_grp.add_argument('-d', '--debug', action='store_true', help='print debugging information')
    parser.add_argument('-nc', '--no-cbus', action='store_true', help='do not change cbus pins')
    dbg_grp.add_argument('-v', '--verbose', action='store_true', help='try to be a bit more verbose')
    parser.add_argument('-p', '--port', metavar='PATH', help='serial device to connect', required=True)
    parser.add_argument('binary', metavar='PATH', help='binary firmware to transfer')
    
    args = parser.parse_args()

    bsl = DnBsl()

    root_logger = logging.getLogger('')
    handler = logging.StreamHandler()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.ERROR)
    bsl.verbose = 0

    if args.verbose:
        bsl.verbose = 1
        root_logger.setLevel(logging.INFO)

    if args.debug:
        bsl.verbose = 3
        root_logger.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('[%(filename)s:%(lineno)d] %(message)s'))

    if not args.no_cbus:
        ftdicbus.set_cbus_pins(args.port, ftdicbus.MSP430_BSL_MODE)
    try:
        bsl.create_option_parser()
        bsl.add_extra_options()

        bsl.add_dn_options(args.port, args.binary)
        bsl.do_the_work()
    finally:
        if not args.no_cbus:
            ftdicbus.set_cbus_pins(args.port, ftdicbus.MSP430_UART_MODE)

if __name__ == '__main__':
    main()
