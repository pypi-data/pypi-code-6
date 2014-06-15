# -*- coding: utf-8 -*-
#
import logging, logging.handlers, sys

exception = logging.exception
error = logging.error
warning = logging.warning
info = logging.info
debug = logging.debug

def logger_init():
    logger = logging.getLogger()
    err_fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # Controllo su quale sistema operativo mi  trovo
    # e carico l'handler corretto
    # (platform restituisce 'win32' o 'linux2')
    if sys.platform == 'win32':
        # Istanzio l'handler per windows
        #
        win_ev_handler = logging.handlers.NTEventLogHandler("Jumbo")
        win_ev_handler.setFormatter(err_fmt)
        logger.addHandler(win_ev_handler)
        # win_file_handler = logging.FileHandler("fatty.log")
        # win_file_handler.setFormatter(err_fmt)
        # logger.addHandler(win_file_handler)

    else:
        # Sono su piattaforma linux
        sys_ev_handler = logging.FileHandler('/tmp/dlight.log')
        sys_fmt = logging.Formatter('Jumbo - %(module)s: %(message)s')
        sys_ev_handler.setFormatter(sys_fmt)
        logger.addHandler(sys_ev_handler)

    err_handler = logging.StreamHandler()
    err_handler.setFormatter(err_fmt)
    err_handler.setLevel(logging.DEBUG)
    logger.addHandler(err_handler)

    logger.setLevel(logging.DEBUG)

logger_init()
