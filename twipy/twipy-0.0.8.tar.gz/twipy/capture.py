# -*- coding: utf-8 -*-

import time
import signal


SECONDS = 2


class CaptureSignals():

    def __init__(self):
        pass

    @staticmethod
    def capture_signals():
        signal.signal(signal.SIGINT, signal_handler_interrupt)


def signal_handler_interrupt(signal, frame):
    print '\nUps! You\'ve pressed Ctrl+C, but it doesn\'t work here... Try with the \'q\' command to quit\n'
    time.sleep(SECONDS)
    pass


def servernotfound_exception():
    print '\nSorry, the tweet in the coconut couldn\'t reach its destination because ' \
          'the swallow was too small to carry it\n'
    print 'Is your Internet conection working well and you fed the swallows?'
    time.sleep(SECONDS)
    return None


def eoferror_exception():
    print 'Don\'t do that, please'
    time.sleep(SECONDS)
    pass
