#!/bin/python
#-*- coding: utf-8 -*-

from amqp.logconsole import LogConsole
from configJSON import ConfigJSON
from toolbox import printu

import sys
import os.path

if __name__ == '__main__':
    if os.path.exists(sys.argv[1]):
        filename = sys.argv[1]
    else:
        filename = os.path.join(    os.path.dirname(__file__),
                                    'simpleamqplogconsole.conf.json')

    cfgfile = ConfigJSON(filename)
    if cfgfile.exists():
        conf = cfgfile.load()
        logconsole = LogConsole(conf)
        logconsole.run()
    else:
        printu(u'Cannot read configuration file "%s"' % (filename))
