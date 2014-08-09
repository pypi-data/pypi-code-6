#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Kamil Chmielewski <kamil.chm@gmail.com>'

from service_discovery import ServiceDiscovery

sd = ServiceDiscovery('/pl/pl/microhackaton', 'zookeeper.microhackathon.pl:2181')

print sd.get_instance('blog-collector')

print sd.register('aaa2', 'aaa2.pl', 8080)

print sd.get_instances('aaa2')

import time
time.sleep(10)
