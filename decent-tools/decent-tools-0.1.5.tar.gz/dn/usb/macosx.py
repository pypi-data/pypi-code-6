"""
Implementation using OSX command line tools
to manage FTDIUSBSerialDriver. As kextunload and kextload
requires root privilege, one can use this module with sudo
or change the /etc/sudoers file accordingly:

your_login ALL=(ALL) NOPASSWD: /sbin/kextload, /sbin/kextunload

"""

import subprocess
from common import wait_for_driver
import logging

logger = logging.getLogger(__name__)

FTDI_BUNDLE_ID = 'com.FTDI.driver.FTDIUSBSerialDriver'
APPLE_FTDI_BUNDLE_ID = 'com.apple.driver.AppleUSBFTDI'

KEXT_FIND = '/usr/sbin/kextfind'
KEXT_UNLOAD = '/sbin/kextunload'
KEXT_LOAD = '/sbin/kextload'

try_bundle = lambda b: len(subprocess.check_output([KEXT_FIND, '-b', b])) > 0

CURRENT_BUNDLE_ID = (
    FTDI_BUNDLE_ID if try_bundle(FTDI_BUNDLE_ID)
    else (
        APPLE_FTDI_BUNDLE_ID if try_bundle(APPLE_FTDI_BUNDLE_ID) 
        else None
        )
    )

logger.debug('{} is selected as the corresponding kernel driver'.format(CURRENT_BUNDLE_ID))

def detach_kernel_driver(serial):
    if is_kernel_driver_active(serial):
        if subprocess.call(["sudo", KEXT_UNLOAD, "-b", CURRENT_BUNDLE_ID]) != 0:
            logger.warning('Kernel driver not properly detached. Proceeding anyways')
        else:
            logger.debug('Kernel driver detached')
    else:
        logger.warning('Kernel driver already detached')

def is_kernel_driver_active(serial):
    loaded = subprocess.check_output([KEXT_FIND, '-loaded', '-b', CURRENT_BUNDLE_ID])
    return len(loaded) > 0

def attach_kernel_driver(path, serial):
    if not is_kernel_driver_active(serial):
        logger.debug('Attaching kernel driver')
        if subprocess.call(["sudo", KEXT_LOAD, "-b", CURRENT_BUNDLE_ID]) != 0:
            logger.warning('Kernel driver not properly attached. Proceeding anyways')
        wait_for_driver(path)
    if is_kernel_driver_active(serial):
        logger.debug('Kernel driver attached')
