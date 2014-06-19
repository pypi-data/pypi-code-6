# -*- coding: utf-8 -*-

# Resource object code
#
# Created: Do. Juni 19 04:51:24 2014
#      by: The Resource Compiler for PySide (Qt v4.8.6)
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore

qt_resource_data = b"\x00\x00\x01\x16Colorless\x0agreen\x0aideas\x0asleep\x0afuriously\x0aA\x0acolorless\x0agreen\x0aidea\x0ais\x0aa\x0anew\x0auntried\x0aidea\x0athat\x0ais\x0awithout\x0avividness\x0adull\x0aand\x0aunexciting\x0aTo\x0asleep\x0afuriously\x0amay\x0aseem\x0aa\x0apuzzling\x0aturn\x0aof\x0aphrase\x0abut\x0athe\x0amind\x0ain\x0asleep\x0aoften\x0aindeed\x0amoves\x0afuriously\x0awith\x0aideas\x0aand\x0aimages\x0aflickering\x0ain\x0aand\x0aout\x0a"
qt_resource_name = b"\x00\x0a\x0b\x0b\x17\xd9\x00d\x00i\x00c\x00t\x00i\x00o\x00n\x00a\x00r\x00y\x00\x09\x08\xb6\xa74\x00w\x00o\x00r\x00d\x00s\x00.\x00t\x00x\x00t"
qt_resource_struct = b"\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
