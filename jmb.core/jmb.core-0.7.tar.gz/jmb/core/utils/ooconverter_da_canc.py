# OpenOffice Converter.
#
# Based on code from:
#   PyODConverter (Python OpenDocument Converter) v1.0.0 - 2008-05-05
#   Start/Stop/Connecting to OpenOffice from http://www.linuxjournal.com/content/starting-stopping-and-connecting-openoffice-python
#
#   Copyright (C) 2009 Thunder Systems <info@thundersystems.it>
#   Licensed under the GNU LGPL v2.1 - or any later version.
#   http://www.gnu.org/licenses/lgpl-2.1.html

from django.conf import settings
import sys
import os
import time
import atexit
import zipfile

DEFAULT_OPENOFFICE_PORT = 2002

# Find OpenOffice.
_oopaths_default=(
        ('/usr/lib64/ooo-2.0/program',   '/usr/lib64/ooo-2.0/program'),
        ('/opt/openoffice.org3/program', '/opt/openoffice.org/basis3.0/program'),
        ('/usr/lib/openoffice/program', '/usr/lib/openoffice/program'),
     )

_oopaths = getattr(settings, 'OOPATHS_DEFAULT', _oopaths_default)

for p in _oopaths:
    if os.path.exists(p[0]):
        OPENOFFICE_PATH    = p[0]
        OPENOFFICE_BIN     = os.path.join(OPENOFFICE_PATH, 'soffice')
        OPENOFFICE_LIBPATH = p[1]

        # Add to path so we can find uno.
        if sys.path.count(OPENOFFICE_LIBPATH) == 0:
            sys.path.insert(0, OPENOFFICE_LIBPATH)
        break

import uno
from os.path import abspath, isfile, splitext
from com.sun.star.beans import PropertyValue
from com.sun.star.task import ErrorCodeIOException
from com.sun.star.connection import NoConnectException

FAMILY_TEXT = "Text"
FAMILY_SPREADSHEET = "Spreadsheet"
FAMILY_PRESENTATION = "Presentation"
FAMILY_DRAWING = "Drawing"

FILTER_MAP = {
    "pdf": {
        FAMILY_TEXT: "writer_pdf_Export",
        FAMILY_SPREADSHEET: "calc_pdf_Export",
        FAMILY_PRESENTATION: "impress_pdf_Export",
        FAMILY_DRAWING: "draw_pdf_Export"
    },
    "html": {
        FAMILY_TEXT: "HTML (StarWriter)",
        FAMILY_SPREADSHEET: "HTML (StarCalc)",
        FAMILY_PRESENTATION: "impress_html_Export"
    },
    "odt": { FAMILY_TEXT: "writer8" },
    "doc": { FAMILY_TEXT: "MS Word 97" },
    "rtf": { FAMILY_TEXT: "Rich Text Format" },
    "txt": { FAMILY_TEXT: "Text" },
    "ods": { FAMILY_SPREADSHEET: "calc8" },
    "xls": { FAMILY_SPREADSHEET: "MS Excel 97" },
    "odp": { FAMILY_PRESENTATION: "impress8" },
    "ppt": { FAMILY_PRESENTATION: "MS PowerPoint 97" },
    "swf": { FAMILY_PRESENTATION: "impress_flash_Export" }
}
# see http://wiki.services.openoffice.org/wiki/Framework/Article/Filter
# for more available filters

class OORunner:
    """
    Start, stop, and connect to OpenOffice.
    """
    def __init__(self, port=DEFAULT_OPENOFFICE_PORT):
        """ Create OORunner that connects on the specified port. """
        self.port = port


    def connect(self, no_startup=False):
        """
        Connect to OpenOffice.
        If a connection cannot be established try to start OpenOffice.
        """
        localContext = uno.getComponentContext()
        resolver     = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext)
        context      = None
        did_start    = False

        n = 0
        while n < 6:
            try:
                context = resolver.resolve("uno:socket,host=localhost,port=%d;urp;StarOffice.ComponentContext" % self.port)
                break
            except NoConnectException:
                pass

            # If first connect failed then try starting OpenOffice.
            if n == 0:
                # Exit loop if startup not desired.
                if no_startup:
                     break
                self.startup()
                did_start = True

            # Pause and try again to connect
            time.sleep(1)
            n += 1

        if not context:
            raise Exception, "Failed to connect to OpenOffice on port %d" % self.port

        desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)

        if not desktop:
            raise Exception, "Failed to create OpenOffice desktop on port %d" % self.port

        if did_start:
            _started_desktops[self.port] = desktop

        return desktop


    def startup(self):
        """
        Start a headless instance of OpenOffice.
        """
        args = [OPENOFFICE_BIN,
                '-accept=socket,host=localhost,port=%d;urp;StarOffice.ServiceManager' % self.port,
                '-norestore',
                '-nofirststartwizard',
                '-nologo',
                '-headless',
                ]
        env  = {'PATH'       : '/bin:/usr/bin:%s' % OPENOFFICE_PATH,
                'PYTHONPATH' : OPENOFFICE_LIBPATH,
                }

        try:
            pid = os.spawnve(os.P_NOWAIT, args[0], args, env)
        except Exception, e:
            raise Exception, "Failed to start OpenOffice on port %d: %s" % (self.port, e.message)

        if pid <= 0:
            raise Exception, "Failed to start OpenOffice on port %d" % self.port


    def shutdown(self):
        """
        Shutdown OpenOffice.
        """
        try:
            if _started_desktops.get(self.port):
                _started_desktops[self.port].terminate()
                del _started_desktops[self.port]
        except Exception, e:
            pass

# Keep track of started desktops and shut them down on exit.
_started_desktops = {}

def _shutdown_desktops():
    """ Shutdown all OpenOffice desktops that were started by the program. """
    for port, desktop in _started_desktops.items():
        try:
            if desktop:
                desktop.terminate()
        except Exception, e:
            pass


atexit.register(_shutdown_desktops)


def oo_shutdown_if_running(port=DEFAULT_OPENOFFICE_PORT):
    """ Shutdown OpenOffice if it's running on the specified port. """
    oorunner = OORunner(port)
    try:
        desktop = oorunner.connect(no_startup=True)
        desktop.terminate()
    except Exception, e:
        pass


def oo_properties(**args):
    """
    Convert args to OpenOffice property values.
    """
    props = []
    for key in args:
        prop       = PropertyValue()
        prop.Name  = key
        prop.Value = args[key]
        props.append(prop)

    return tuple(props)


class DocumentConversionException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class DocumentConverter:
    def __init__(self, port=DEFAULT_OPENOFFICE_PORT):
        self.oorunner = OORunner()
        self.desktop = self.oorunner.connect()

    def convert(self, inputFile, outputFile):

        inputUrl = self._toFileUrl(inputFile)
        outputUrl = self._toFileUrl(outputFile)

        document = self.desktop.loadComponentFromURL(inputUrl, "_blank", 0, self._toProperties(Hidden=True))

        try:
          document.refresh()
        except AttributeError:
          pass

        outputExt = self._getFileExt(outputFile)
        filterName = self._filterName(document, outputExt)

        try:
            document.storeToURL(outputUrl, self._toProperties(FilterName=filterName))
        finally:
            document.close(True)
            self.oorunner.shutdown()

    def _filterName(self, document, outputExt):
        family = self._detectFamily(document)
        try:
            filterByFamily = FILTER_MAP[outputExt]
        except KeyError:
            raise DocumentConversionException, "unknown output format: '%s'" % outputExt
        try:
            return filterByFamily[family]
        except KeyError:
            raise DocumentConversionException, "unsupported conversion: from '%s' to '%s'" % (family, outputExt)

    def _detectFamily(self, document):
        if document.supportsService("com.sun.star.text.GenericTextDocument"):
            # NOTE: a GenericTextDocument is either a TextDocument, a WebDocument, or a GlobalDocument
            # but this further distinction doesn't seem to matter for conversions
            return FAMILY_TEXT
        if document.supportsService("com.sun.star.sheet.SpreadsheetDocument"):
            return FAMILY_SPREADSHEET
        if document.supportsService("com.sun.star.presentation.PresentationDocument"):
            return FAMILY_PRESENTATION
        if document.supportsService("com.sun.star.drawing.DrawingDocument"):
            return FAMILY_DRAWING
        raise DocumentConversionException, "unknown document family: %s" % document

    def _getFileExt(self, path):
        ext = splitext(path)[1]
        if ext is not None:
            return ext[1:].lower()

    def _toFileUrl(self, path):
        return uno.systemPathToFileUrl(abspath(path))

    def _toProperties(self, **args):
        props = []
        for key in args:
            prop = PropertyValue()
            prop.Name = key
            prop.Value = args[key]
            props.append(prop)
        return tuple(props)

if __name__ == "__main__":
    from sys import argv, exit

    if len(argv) < 3:
        print "USAGE: python %s <input-file> <output-file>" % argv[0]
        exit(255)
    if not isfile(argv[1]):
        print "no such input file: %s" % argv[1]
        exit(1)

    try:
        converter = DocumentConverter()
        converter.convert(argv[1], argv[2])
    except DocumentConversionException, exception:
        print "ERROR!" + str(exception)
        exit(1)
    except ErrorCodeIOException, exception:
        print "ERROR! ErrorCodeIOException %d" % exception.ErrCode
        exit(1)

