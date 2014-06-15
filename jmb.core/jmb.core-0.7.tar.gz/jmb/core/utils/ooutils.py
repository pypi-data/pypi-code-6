# coding: utf-8
"""
.. _ooutils:

OpenOffice utils
=================

Queste utility permettono di connettersi ad un server OpenOffice/Libreoffice
tramite il modulo python ``uno``.

.. note:: Monkey-patch

  questo modulo fa mankey-patching del meccanismo di import per cui ogni errore successivo 
  e **scorrelato** di import viene  erroneamente fatto risalire al modulo uno

  Per questo ho fatto attenzione a non avere alcun import di 'uno' o di 'com.sun.*'
  durante l'import di questo modulo. 
        
functions
---------

Il modo normale di usare questo modulo è tramite la vista

.. autofunction:: jmb.core.views.generic.create_oo_file.create_file

Uso
----

Esiste anche una vista che permette di ritornare direttamente il contenuto
come pdf:

.. automodule:: jmb.core.views.generic.create_oo_file

"""
import sys
import os
import time
import atexit
import zipfile

from django.conf import settings
from django.http import HttpResponse

# OpenOffice Converter.
#
# Based on code from:
#   PyODConverter (Python OpenDocument Converter) v1.0.0 - 2008-05-05
#   Start/Stop/Connecting to OpenOffice from http://www.linuxjournal.com/content/starting-stopping-and-connecting-openoffice-python
#
#   Copyright (C) 2009 Thunder Systems <info@thundersystems.it>
#   Licensed under the GNU LGPL v2.1 - or any later version.
#   http://www.gnu.org/licenses/lgpl-2.1.html


DEFAULT_OPENOFFICE_PORT = getattr(settings, 'DEFAULT_OPENOFFICE_PORT', 8100)

# Find OpenOffice.
_oopaths_default=(
        ('/usr/lib64/ooo-2.0/program',   '/usr/lib64/ooo-2.0/program'),
        ('/opt/openoffice.org3/program', '/opt/openoffice.org/basis3.0/program'),
        ('/usr/lib/openoffice/program', '/usr/lib/openoffice/program'),
        ('/usr/lib/libreoffice/program', '/usr/lib/libreoffice/program'),
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
################################################################################# 
### NON Scommentare senza avere capito bene la nota nella docstring del modulo
################################################################################# 
#import uno

from os.path import abspath, isfile, splitext

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
        import uno
        from com.sun.star.connection import NoConnectException

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
    import uno
    PropertyValue = uno.getClass('com.sun.star.beans.PropertyValue')

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
        AUTOMATIC_STARTUP_OPENOFFICE = getattr(settings, 'AUTOMATIC_STARTUP_OPENOFFICE', False)
        self.oorunner = OORunner()
        self.desktop = self.oorunner.connect(no_startup=not AUTOMATIC_STARTUP_OPENOFFICE)

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
        import uno
        return uno.systemPathToFileUrl(abspath(path))

    def _toProperties(self, **args):
        import uno
        PropertyValue = uno.getClass('com.sun.star.beans.PropertyValue')

        props = []
        for key in args:
            prop = PropertyValue()
            prop.Name = key
            prop.Value = args[key]
            props.append(prop)
        return tuple(props)

class OOUtils(object):
    def _get_string_odt(self, request, file_modello=None, obj=None, language=None, path_modello=None, extra_context={}):
        from jmb.core.shortcuts import render_from_string
        from StringIO import StringIO
        from django.utils import translation
        # Recupero il percorso assoluto del template in odt per poi passarlo
        # alla funzione che mi creera' il nuovo odt con i dati dell'utente
        if not path_modello:
            from jmb.core.utils.functions import get_template_abspath
            file_modello = get_template_abspath(file_modello)
        else:
            file_modello = path_modello

        cur_language = translation.get_language()
        if language:
            try:
                translation.activate(language)
            except:
                pass

        bufferr = StringIO()

        # Apro il file MODELLO in lettura per poter poi creare il nuovo file
        # con tt i file identici al nuovo, ma con il file content.xml generato
        # attraverso il giro dei template di Django
        oofile_modello = zipfile.ZipFile(file_modello, 'r')

        # Creo il nuovo zip
        oofile_new = zipfile.ZipFile(bufferr, 'w')
        new_content_xml = ""

        # Ciclo tt i file presenti nel modello e li aggiungo al nuovo
        # odt. Tutti i file verranno presi cosi come sono in originale,
        # tranne il file content.xml che sara' prima parsato per generare
        # i dati utente
        for info in oofile_modello.infolist():
            if info.filename == "content.xml":
                data = oofile_modello.read(info.filename) #.decode('latin-1')
                data = self._replace_entities(data)
                new_content_xml = render_from_string(
                    data, request, obj=obj, **extra_context
                )

            elif info.filename == "styles.xml":
                data = oofile_modello.read(info.filename) #.decode('latin-1')
                new_styles_xml = render_from_string(
                    data, request, obj=obj, **extra_context
                )
            else:
                data = oofile_modello.read(info.filename)
                oofile_new.writestr(info.filename, data)

        # Il contenuto creato e' tutto in utf-8, ma StringIO accetta solo ascii e quindi
        # bisogna convertire tutto
        oofile_new.writestr("content.xml", new_content_xml.encode('utf-8'))
        oofile_new.writestr("styles.xml", new_styles_xml.encode('utf-8'))
        oofile_new.close()

        bufferr.flush()
        ret_oofile = bufferr.getvalue()
        bufferr.close()

        # Riattivo il linguaggio di default
        translation.activate(cur_language)
        return ret_oofile

    def _replace_entities(self, data):
        """
        replace special entities
        """
        entities = (('&quot;','"'),('&apos;',"'"),) # TODO: valutare se lasciare qui o spostare nei settings
        for entity in entities:
            data = data.replace(entity[0], entity[1])
        return data

    def save_odt(self, request, file_modello=None, f_name='convert', obj=None, get_raw_string=False,
                 language=None, save_in=None, path_modello = None, extra_context={}):
        str_oofile = self._get_string_odt(request, file_modello, obj=obj, language=language, path_modello=path_modello, extra_context=extra_context)
        if get_raw_string:
            return str_oofile

        if save_in:
            path_file = os.path.join(save_in, f_name)
            ff = open(path_file, 'w')
            ff.write(str_oofile)
            ff.close()

        response = HttpResponse(mimetype='application/x-zip-compressed')
        response['Content-Disposition'] = 'attachment; filename=%s.odt' % f_name
        response.write(str_oofile)
        return response

    def save_ods(self, request, file_modello=None, f_name='convert', obj=None, get_raw_string=False,
                 language=None, save_in=None, path_modello = None, extra_context={}):
        str_oofile = self._get_string_odt(request, file_modello, obj=obj, language=language, path_modello=path_modello, extra_context=extra_context)
        if get_raw_string:
            return str_oofile

        if save_in:
            path_file = os.path.join(save_in, f_name)
            ff = open(path_file, 'w')
            ff.write(str_oofile)
            ff.close()

        response = HttpResponse(mimetype='application/x-zip-compressed')
        response['Content-Disposition'] = 'attachment; filename=%s.ods' % f_name
        response.write(str_oofile)
        return response

    def save_pdf(self, request=None, file_modello=None, f_name='convert', obj=None, get_raw_string=False,
                 language=None, save_in=None, path_modello = None, extra_context={}):
        """
        Return the path of a file generated. Differs from save_pdf_new as it does not return a 
        response 

        :arg request: a HttpRequest - Not needed
        :arg file_modello:
        :arg f_name: the file of the destination name
        :arg obj: the object put in the context
        :arg get_raw_string: return the handle to output file
        :arg language: a possible language to be activated when rendering
        :arg save_in: a directory where the output should be generated
        :arg path_modello: ???
        :arg extra_content: extra content used when rendering the template
        """
        import tempfile

        t_in = tempfile.NamedTemporaryFile(mode='w+b', suffix='.odt')
        t_out = tempfile.NamedTemporaryFile(mode='w+b', suffix='.pdf')

        str_oofile = self._get_string_odt(request, file_modello, obj=obj, language=language, path_modello=path_modello, extra_context=extra_context)
        t_in.write(str_oofile)
        t_in.seek(0)

        d = DocumentConverter()
        d.convert(t_in.name, t_out.name)

        t_out.seek(0)

        if get_raw_string:
            return t_out

        if save_in:
            path_file = os.path.join(save_in, f_name)
            ff = open(path_file, 'w')
            ff.write(t_out.read())
            ff.close()

        # Ritorno il file pdf da scaricare
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s.pdf' % f_name
        response.write(t_out.read())
        return response

    def save_pdf_new(self, request, file_modello=None, f_name='convert', obj=None, get_raw_string=False,
                 language=None, save_in=None, path_modello = None, extra_context={}):
        # Import qua shlex e subprocess per evitare errori di import in vecchie installazione che usano ancora l'altra funzione
        import tempfile, shlex, subprocess
        t_in = tempfile.NamedTemporaryFile(mode='w+b', suffix='.odt')
        # Il comando di conversione crea un file con lo stesso nome del t_in ma con estensione .pdf
        t_out_name = t_in.name.replace('.odt', '.pdf')

        str_oofile = self._get_string_odt(request, file_modello, obj=obj, language=language, path_modello=path_modello, extra_context=extra_context)
        t_in.write(str_oofile)
        t_in.seek(0)

        cmd = shlex.split("libreoffice --headless -convert-to pdf:writer_pdf_Export -outdir /tmp %s" % t_in.name)
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if not output.find("convert ") > -1 or error != '':
            raise Exception("Something goes wrong during pdf conversion")

        t_out = open(t_out_name, 'r')
        if get_raw_string:
            return t_out

        if save_in:
            path_file = os.path.join(save_in, f_name)
            ff = open(path_file, 'w')
            ff.write(t_out.read())
            ff.close()

        # Ritorno il file pdf da scaricare
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s.pdf' % f_name
        response.write(t_out.read())
        return response

    def save_pdf2(self, request=None, template_file=None, destination_name='convert', obj=None, 
                 language=None, save_in=None, extra_context={}):
        """
        Return the path of a file generated. Differs from save_pdf_new as it does not return a 
        response 

        :arg request: a HttpRequest - Not needed
        :arg template_file:
        :arg destination_name: the file of the destination name
        :arg obj: the object put in the context
        :arg language: a possible language to be activated when rendering
        :arg save_in: a directory where the output should be generated
        :arg extra_content: extra content used when rendering the template
        """
        # Import qua shlex e subprocess per evitare errori di import in vecchie installazione che usano ancora l'altra funzione

        import tempfile, shlex, subprocess

        t_in = tempfile.NamedTemporaryFile(mode='w+b', suffix='.odt')
        # Il comando di conversione crea un file con lo stesso nome del t_in ma con estensione .pdf
        t_out_name = t_in.name.replace('.odt', '.pdf')

        str_oofile = self._get_string_odt(None, template_file, obj=obj, language=language, extra_context=extra_context)
        t_in.write(str_oofile)
        t_in.seek(0)

        cmd = shlex.split("libreoffice --headless --convert-to pdf:writer_pdf_Export --outdir /tmp %s" % t_in.name)
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if 'convert' not in output or (error and 'warning' not in error):
            raise Exception("Something goes wrong during pdf conversion")

        t_out = open(t_out_name, 'r')

        if save_in:
            path_file = os.path.join(save_in, dest_name)
            ff = open(path_file, 'w')
            ff.write(t_out.read())
            ff.close()
            return path_file
        return t_out.name

if __name__ == "__main__":
    from sys import argv, exit

    import uno
    from com.sun.star.task import ErrorCodeIOException

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

