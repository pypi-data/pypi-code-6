#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Kamil Chmielewski <kamil.chm@gmail.com>'

from service_discovery import ServiceDiscovery

sd = ServiceDiscovery('/pl/pl/microhackaton', 'zookeeper.microhackathon.pl:2181')

print sd.get_instance('blog-collector')
