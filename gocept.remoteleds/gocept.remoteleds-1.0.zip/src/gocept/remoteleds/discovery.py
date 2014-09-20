#!/usr/bin/python
# coding: utf-8

import serial
import serial.tools.list_ports
import time
import gocept.remoteleds.client
import gocept.remoteleds.config
from .log import log

BAUD = 57600
SCAN_DELAY_IN_S = 1


def main():
    cfg = gocept.remoteleds.config.Config()
    cfg.load()
    dev = discover_loop(cfg.serial_number)
    connect(cfg, dev)


def discover_loop(snr):
    dev = None
    while dev is None:
        dev = discover(snr)
        time.sleep(SCAN_DELAY_IN_S)
    return dev

def discover(serial_number):
    comports = list(serial.tools.list_ports.comports())
    print comports
    for port in comports:
        if "SNR={}".format(serial_number) in port[2]:
            return port[0]
    return None

def connect(cfg, dev):
    if dev is not None:
        try:
            connection = serial.Serial(dev, BAUD)

            log.info("Waiting for Handshake")
            while (connection.readline().strip() != 'PING'):
                time.sleep(0.1)

            log.info("Answer Handshake")
            connection.write("14")
            connection.flushInput()

            while ("READY" not in connection.readline()):
                time.sleep(0.1)
            log.info("Connection ready")

            clients = []
            for client_cfg in cfg.clients:
                client_cls = gocept.remoteleds.config.AVAILABLE[client_cfg['type']]
                clients.append(client_cls(connection=connection, config=client_cfg))
            tick = 0
            while True:
                tick += 1
                for cli in clients:
                    cli.update(tick)
                connection.write("FLU\n")
                time.sleep(0.05)
                if tick == 105:
                    tick = 0
            connection.close()
        except serial.serialutil.SerialException as e:
            log.debug(str(e))
            dev = discover_loop(cfg.serial_number)
            connect(cfg, dev)


if __name__ == '__main__':
    main()
