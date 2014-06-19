# -*- coding: utf-8 -*-

# Resource object code
#
# Created: Do. Juni 19 09:54:13 2014
#      by: The Resource Compiler for PySide (Qt v4.8.6)
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore

qt_resource_data = b"\x00\x00\x00\xf7Qt\x0aQuarterly\x0ais\x0aa\x0apaper\x0abased\x0anewsletter\x0aexclusively\x0aavailable\x0ato\x0aQt\x0acustomers\x0aEvery\x0aquarter\x0awe\x0amail\x0aout\x0aan\x0aissue\x0athat\x0awe\x0ahope\x0awill\x0abring\x0aadded\x0ainsight\x0aand\x0apleasure\x0ato\x0ayour\x0aQt\x0aprogramming\x0awith\x0ahigh\x0aquality\x0atechnical\x0aarticles\x0awritten\x0aby\x0aQt\x0aexperts\x0a"
qt_resource_name = b"\x00\x0a\x0b\x0b\x17\xd9\x00d\x00i\x00c\x00t\x00i\x00o\x00n\x00a\x00r\x00y\x00\x09\x08\xb6\xa74\x00w\x00o\x00r\x00d\x00s\x00.\x00t\x00x\x00t"
qt_resource_struct = b"\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
