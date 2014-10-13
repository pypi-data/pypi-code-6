#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import subprocess
from queue import Queue
import bottle
from pymobile import shared
from models import devicelist

devices = devicelist.getDevices()
cmd = Queue()


@bottle.route('/wol')
@bottle.route('/wol/')
@bottle.view('wol')
def wol():
    ''' Lister opp alle pc-er '''
    user = shared.session['user']
    if not user:
       bottle.abort(401)
    else:
        return dict(user=user, devices=devices)


@bottle.route('/wol/<mac>')
@bottle.view('dialog')
def runwol(mac):
    ''' tar imot wake on lan kommando og oppdaterer liste '''
    user = shared.session['user']
    til = ""
    if not user:
       bottle.abort(401)
    else:
        for dev in devices:
            if dev.mac == mac:
                cmd.put(["wakeonlan", mac])
                dev.stop = False
                dev.start = True
                til = dev.name
                
        return dict(
            title='Send startkommando',
            content='Start-kommando sendt til {}'.format(til),
            okbutton=True)


@bottle.route('/shutdown/<ip>')
@bottle.view('dialog')
def runshutdown(ip):
    ''' tar imot shutdown kommando og oppdaterer liste '''
    user = shared.session['user']
    til = ""
    if not user:
       bottle.abort(401)
    else:
        for dev in devices:
            if dev.ip == ip:
                cmd.put(['ssh', '-o', 'PasswordAuthentication=no', 'root@{}'.format(ip), 'shutdown -h now'])
                dev.start = False
                dev.stop = True
                til = dev.name
                
        return dict(
            title='Send stoppkommando',
            content='Stopp-kommando sendt til {}'.format(til),
            okbutton=True)


@shared.worker
def wol():
    while not shared.stop.wait(0.2):
        if not cmd.empty():
            command = cmd.get()
            logging.info('command {!r}'.format(command))
            try:
                res = subprocess.check_output(
                    command,
                    stdin=None,
                    universal_newlines=True)
                logging.info('res: {}{!r}'.format(command[0], res))
            except OSError as e:
                logging.error('{}{!r}'.format(command[0], e))
            except subprocess.CalledProcessError as e:
                logging.error('{}{!r}'.format(command[0], e))


@shared.worker
def fast_pinger():
    while not shared.stop.wait(1): # hvert sekund
        for dev in devices:
            if dev.start or dev.stop or (not dev.up and not dev.down):
                try:
                    logging.debug('ping {}'.format(dev.ip))
                    subprocess.check_output(["ping", "-c", "1", "-t", "1", dev.ip])
                    isUp = True
                except subprocess.CalledProcessError as e:
                    isUp = False
                finally:
                    dev.update(isUp)

@shared.worker
def slow_pinger():
    while not shared.stop.wait(60): # ett minutt
        for dev in devices:
            try:
                logging.debug('ping {}'.format(dev.ip))
                subprocess.check_output(["ping", "-c", "1", "-t", "1", dev.ip])
                isUp = True
            except subprocess.CalledProcessError as e:
                isUp = False
            finally:
                dev.update(isUp)

@shared.worker
def nmap_discovery():
    devicelist.updateDevicesFromNmap() #this will update devices-variable
