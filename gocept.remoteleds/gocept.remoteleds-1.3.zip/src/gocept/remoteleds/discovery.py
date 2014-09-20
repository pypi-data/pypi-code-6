#!/usr/bin/python
# coding: utf-8
import argparse
import os
import serial
import serial.tools.list_ports
import time
import gocept.remoteleds.client
import gocept.remoteleds.config
from .log import log

BAUD = 57600
SCAN_DELAY_IN_S = 1


def main(config_path):
    cfg = gocept.remoteleds.config.Config(os.path.expanduser(config_path))
    cfg.load()
    dev = discover_loop(cfg.serial_number)
    connect(cfg, dev)

def list_comports():
    comports = list(serial.tools.list_ports.comports())
    return [port for port in comports if 'SNR' in port[2]]

def discover_loop(snr):
    dev = None
    log.info('Waiting for available COM Ports changes.')
    current_ports = []
    while dev is None:
        new_comports = list_comports()
        if current_ports == new_comports:
            continue
        log.info('COM Port scan result:\n{}'.format(
                  '\n'.join(['{} {} {}'.format(*port) for port in new_comports])))
        current_ports = new_comports
        dev = discover(snr, current_ports)
        time.sleep(SCAN_DELAY_IN_S)
    return dev

def discover(serial_number, current_ports):
    for port in current_ports:
        if "SNR={}".format(serial_number) in port[2]:
            log.info('Found {} on COM Port {}.'.format(serial_number, port[0]))
            return port[0]
        else:
            log.info('No COM Port matching SNR {} found.'.format(serial_number))
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
            log.info('Connection lost, reinitiating COM Port scanning.')
            dev = discover_loop(cfg.serial_number)
            connect(cfg, dev)

def entry():
    parser = argparse.ArgumentParser(description='Client for RemoteLEDs Hardware.')
    parser.add_argument(
        '-c', '--config', type=str,
        help='Location for configuration file. '
             'Defaults to {}'.format(os.path.expanduser('~/remoteleds.ini')),
        default='~/remoteleds.ini')
    args = parser.parse_args()
    main(args.config)


if __name__ == '__main__':
    entry()
