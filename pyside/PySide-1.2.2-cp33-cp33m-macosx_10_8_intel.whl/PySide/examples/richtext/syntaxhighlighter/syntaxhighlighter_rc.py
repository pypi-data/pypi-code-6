# -*- coding: utf-8 -*-

# Resource object code
#
# Created: Do. Juni 19 03:42:11 2014
#      by: The Resource Compiler for PySide (Qt v4.8.6)
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore

qt_resource_data = b"\x00\x00\x06yTEMPLATE = app\x0aLANGUAGE = C++\x0aTARGET         = assistant\x0a\x0aCONFIG        += qt warn_on\x0aQT            += xml network\x0a\x0aPROJECTNAME        = Assistant\x0aDESTDIR            = ../../bin\x0a\x0aFORMS += finddialog.ui \x5c\x0a        helpdialog.ui \x5c\x0a        mainwindow.ui \x5c\x0a        settingsdialog.ui \x5c\x0a        tabbedbrowser.ui \x5c\x0a        topicchooser.ui\x0a\x0aSOURCES += main.cpp \x5c\x0a        helpwindow.cpp \x5c\x0a        topicchooser.cpp \x5c\x0a        docuparser.cpp \x5c\x0a        settingsdialog.cpp \x5c\x0a        index.cpp \x5c\x0a        profile.cpp \x5c\x0a        config.cpp \x5c\x0a        finddialog.cpp \x5c\x0a        helpdialog.cpp \x5c\x0a        mainwindow.cpp \x5c\x0a        tabbedbrowser.cpp\x0a\x0aHEADERS        += helpwindow.h \x5c\x0a        topicchooser.h \x5c\x0a        docuparser.h \x5c\x0a        settingsdialog.h \x5c\x0a        index.h \x5c\x0a        profile.h \x5c\x0a        finddialog.h \x5c\x0a        helpdialog.h \x5c\x0a        mainwindow.h \x5c\x0a        tabbedbrowser.h \x5c\x0a        config.h\x0a\x0aRESOURCES += assistant.qrc\x0a\x0aDEFINES += QT_KEYWORDS\x0a#DEFINES +=  QT_PALMTOPCENTER_DOCS\x0a!network:DEFINES        += QT_INTERNAL_NETWORK\x0aelse:QT += network\x0a!xml: DEFINES                += QT_INTERNAL_XML\x0aelse:QT += xml\x0ainclude( ../../src/qt_professional.pri )\x0a\x0awin32 {\x0a    LIBS += -lshell32\x0a    RC_FILE = assistant.rc\x0a}\x0a\x0amac {\x0a    ICON = assistant.icns\x0a    TARGET = assistant\x0a#    QMAKE_INFO_PLIST = Info_mac.plist\x0a}\x0a\x0a#target.path = $$[QT_INSTALL_BINS]\x0a#INSTALLS += target\x0a\x0a#assistanttranslations.files = *.qm\x0a#assistanttranslations.path = $$[QT_INSTALL_TRANSLATIONS]\x0a#INSTALLS += assistanttranslations\x0a\x0aTRANSLATIONS        = assistant_de.ts \x5c\x0a                  assistant_fr.ts\x0a\x0a\x0aunix:!contains(QT_CONFIG, zlib):LIBS += -lz\x0a\x0a\x0atarget.path=$$[QT_INSTALL_BINS]\x0aINSTALLS += target\x0a"
qt_resource_name = b"\x00\x08\x0e\x84\x7fC\x00e\x00x\x00a\x00m\x00p\x00l\x00e\x00s\x00\x07\x0c\xe8G\xe5\x00e\x00x\x00a\x00m\x00p\x00l\x00e"
qt_resource_struct = b"\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x16\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
