# -*- coding: utf-8 -*-

from __future__ import print_function

import glob
import logging
import os
import socket
import subprocess
import sys
import time

log = logging.getLogger(__name__)


class OfficeException(Exception):
    pass


class OfficeBase(object):

    OFFICE_EXE = "soffice"
    OFFICE_UNO_PY = "uno.py"
    OFFICE_PROGAM_PATH = "program"

    SEARCHPATHS_UNIX = \
        glob.glob('/usr/lib*/libreoffice*') + \
        glob.glob('/usr/lib*/openoffice*') + \
        glob.glob('/usr/lib*/ooo*') + \
        glob.glob('/opt/libreoffice*') + \
        glob.glob('/opt/openoffice*') + \
        glob.glob('/opt/ooo*') + \
        glob.glob('/usr/local/libreoffice*') + \
        glob.glob('/usr/local/openoffice*') + \
        glob.glob('/usr/local/ooo*') + \
        glob.glob('/usr/local/lib/libreoffice*')

    SEARCHPATHS_MAC = \
        glob.glob('/Applications/*Office.app/Contents/')

    def is_mac(self):
        return os.name == 'mac' or sys.platform == 'darwin'

    @property
    def searchpaths(self):
        if self.is_mac():
            return self.SEARCHPATHS_MAC

        return self.SEARCHPATHS_UNIX

    @property
    def exepath(self):
        if self.is_mac():
            return "MacOS"

        return self.OFFICE_PROGAM_PATH

    def find_office_path(self):
        for path in self.searchpaths:

            officepath = os.path.join(path, self.exepath)
            if os.path.isfile(os.path.join(officepath, self.OFFICE_EXE)):
                return officepath

        raise OfficeException(
            "Office path not found in %s" % self.searchpaths)

    def find_office_executable(self):
        for path in self.searchpaths:
            exe = os.path.join(path, self.exepath, self.OFFICE_EXE)
            if os.path.isfile(exe):
                return exe

        raise OfficeException(
            "%s executable not found in %s" % (self.OFFICE_EXE,
                                               self.searchpaths))

    def find_pyuno_path(self):
        for path in self.searchpaths:
            program_path = os.path.join(path, self.OFFICE_PROGAM_PATH)
            py_uno = os.path.join(program_path, self.OFFICE_UNO_PY)
            if os.path.isfile(py_uno):
                return program_path

        raise OfficeException(
            "%s not found in %s" % (self.OFFICE_UNO_PY, self.searchpaths))

    def find_python_home(self):
        officepath = self.find_office_path()
        if self.is_mac():
            paths = glob.glob(os.path.join(
                officepath, "*OfficePython.framework"))
        else:
            paths = glob.glob(os.path.join(officepath, "python-core-*"))

        for path in paths:
            if os.path.exists(path):
                return path

        raise OfficeException(
            "Python home not found in %s" % self.searchpaths)

    def find_python_executable(self):
        for path in self.searchpaths:
            opath = os.path.join(path, self.OFFICE_PROGAM_PATH)
            for exe in [os.path.join(opath, "python")] + glob.glob(
                    os.path.join(opath, "python-*")):
                if os.path.isfile(exe):
                    return exe

        raise OfficeException(
            "Python executable not found in %s" % self.searchpaths)

    def find_programm_path(self):
        for path in self.searchpaths:
            program_path = os.path.join(path, self.OFFICE_PROGAM_PATH)
            if os.path.isdir(program_path):
                return program_path

        raise OfficeException(
            "Programm path not found in %s" % self.searchpaths)


class OfficeServer(OfficeBase):

    """
    Starts an Open-/LibreOffice server
    """

    OFFICE_ARG_ACCEPT = "--accept=socket,host=%(host)s,port=%(port)s;urp;" \
                        "StarOffice.ServiceManager"
    OFFICE_ARGS = [
        "--norestore",
        "--nofirststartwizard",
        "--nologo",
        "--invisible"
    ]

    def __init__(self, host="localhost", port=2002, timeout=5.0):
        self.oopid = 0
        self.host = host
        self.port = port
        self.timeout = timeout
        self.cwd = os.getcwd()

    def is_running(self):
        try:
            # try to connect socket to test if ooffice is running
            csocket = socket.create_connection((self.host, self.port),
                                               self.timeout)
            csocket.close()
            log.debug("Existing listener on %s port %s found." % (
                self.host, self.port))
            return True
        except socket.error:
            log.debug("Existing listener on %s port %s not found." % (
                self.host, self.port))
            return False

    def start(self):
        newenv = os.environ.copy()
        # set home directory for running in mod_wsgi
        # the user that executes the process needs write access to /tmp
        # and /tmp/.openoffice.org
        tmpdir = os.path.join("/tmp", self.get_user())
        if not os.path.exists(tmpdir):
            # create dir if it doesn't exist yet because libreoffice will
            # fail to start in that case
            os.mkdir(tmpdir)
        newenv["HOME"] = tmpdir
        exe = self.find_office_executable()

        log.debug("executing command: " + " ".join(
            [exe] + self.OFFICE_ARGS + [self.OFFICE_ARG_ACCEPT % dict(
                host=self.host, port=self.port)]
            )
        )
        proc = subprocess.Popen(
            [exe] + self.OFFICE_ARGS + [self.OFFICE_ARG_ACCEPT % dict(
                host=self.host, port=self.port)], env=newenv,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.oopid = proc.pid

        waited = 0
        started = False
        while waited < 10:
            if proc.poll():
                # process isn't running anymore
                (stdout, stderr) = proc.communicate()
                raise OfficeException("OfficeServer has already "
                                      "terminated. %s" % stderr)

            # check if ooffice is ready yet
            if not self.is_running():
                time.sleep(5)
                waited += 1
            else:
                started = True
                break

        if not started:
            raise OfficeException("Launch of %s failed." % self.OFFICE_EXE)

    def get_user(self):
        env = os.environ
        if "USER" in env:
            user = env["USER"]
        elif "APACHE_RUN_USER" in env:
            user = env["APACHE_RUN_USER"]
        else:
            user = ""
        return user

    def die(self):
        if self.oopid:
            log.debug('Shutting down OfficeServer with pid: %s' %
                      self.oopid)
            try:
                os.kill(self.oopid, 15)
                state = (0, 0)
                waited = 0
                while (state == (0, 0) and waited < 15):
                    log.debug('Waiting for OfficeServer with pid %s '
                              'to disappear.' % self.oopid)
                    state = os.waitpid(self.oopid, os.WNOHANG)
                    if (state != (0, 0)):
                        break
                    waited += 1
                    time.sleep(1)
                else:
                    log.warn("Terminating %s" % self.oopid)
                    os.kill(self.oopid, 9)
            except:
                log.error('Could not find Process %s' % self.oopid)
        else:
            log.debug('OfficeServer is not running')


class Properties(object):

    """
    Class for easier handling of pyuno PropertyValues
    """

    def __init__(self, **kwargs):
        self.props = []

        for name, value in kwargs.items():
            self.add(name, value)

    def add(self, name, value, handle=None, state=None):
        from com.sun.star.beans import PropertyValue

        prop = PropertyValue()
        prop.Name = name
        prop.Value = value
        if handle is not None:
            prop.Handle = handle
        if state is not None:
            prop.State = state
        self.props.append(prop)

    def get_property_values(self):
        return tuple(self.props)

    def __call__(self):
        return self.get_property_values()


class OfficeClient(OfficeBase):

    def __init__(self, host="localhost", port=2002):
        from py3o.formats import Formats
        self.formats = Formats()

        self.host = host
        self.port = port

    def get_py_file(self):
        py_file = __file__
        if py_file.endswith(".pyc"):
            py_file = py_file[:-1]
        return py_file

    def convert(self, infilename, outfilename, format):
        python = self.find_python_executable()
        py_file = self.get_py_file()
        odffilter = self.get_filter(format)

        command = [python, "-B", py_file, self.host, str(self.port),
                   infilename, outfilename, odffilter]

        log.debug("Spawning OfficeClient with command %s" % command)
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
        log.debug(out)
        if proc.returncode != 0:
            raise OfficeException("Spawned client had an error: %s" % err)

    def get_filter(self, format_name):
        from py3o.formats import UnkownFormatException
        try:
            format = self.formats.get_format(format_name)
        except UnkownFormatException:
            raise OfficeException("Format %s is not supported" % format)

        return format.odfname


class OfficeClientSpawned(OfficeBase):

    UNO_RESOLVER = "com.sun.star.bridge.UnoUrlResolver"
    UNO_RESOLVE = "uno:socket,host=%(host)s,port=%(port)s;urp;" + \
        "StarOffice.ComponentContext"
    UNO_DESKTOP = "com.sun.star.frame.Desktop"
    UNO_PATHNAME = "vnd.sun.star.pathname"

    def __init__(self, host="localhost", port=2002):
        self.host = host
        self.port = port
        self.desktop = None

    def is_change_office_env(self):
        return self.find_office_path() in sys.executable

    def connect(self):
        if self.is_change_office_env():
            self.set_office_env()

        import uno
        from com.sun.star.connection import NoConnectException

        localctx = uno.getComponentContext()
        resolver = localctx.ServiceManager.createInstanceWithContext(
            self.UNO_RESOLVER, localctx)
        try:
            ctx = resolver.resolve(self.UNO_RESOLVE % dict(host=self.host,
                                                           port=self.port)
                                   )
        except NoConnectException:
            raise OfficeException("Could not connect to OfficeServer %s on "
                                  "port %s" % (self.host, self.port))
        smgr = ctx.ServiceManager
        self.desktop = smgr.createInstanceWithContext(self.UNO_DESKTOP, ctx)

    def set_office_env(self):
        log.debug("Switching office env")

        uno_path = self.find_pyuno_path()
        pythonhome = self.find_python_home()

        os.environ["UNO_PATH"] = uno_path
        os.environ["PYTHONHOME"] = pythonhome
        os.environ['URE_BOOTSTRAP'] = self.UNO_PATHNAME + ":" + os.path.join(
            uno_path, "fundamentalrc")

        if uno_path not in sys.path:
            sys.path.append(uno_path)

    def is_connected(self):
        return self.desktop is not None

    def convert(self, infilename, outfilename, odffilter):
        inputprops = Properties(Hidden=True, ReadOnly=True)

        document = self.load_document(infilename, inputprops)
        self.update_document(document)
        self.write_document(document, outfilename, odffilter)

    def load_document(self, infilename, inputprops=None):
        inputprops = inputprops or []

        if not os.path.isfile(infilename):
            raise OfficeException("Input file %s does not exist" % infilename)

        in_url = self.path_to_url(infilename)
        document = self.desktop.loadComponentFromURL(in_url, "_blank", 0,
                                                     inputprops())
        if not document:
            raise OfficeException("Input document %s couldn't be loaded" %
                                  in_url)
        return document

    def update_document(self, document):
        # try to refresh the document TOCs and indexes
        try:
            document.refresh()
            indexes = document.getDocumentIndexes()

        except AttributeError:
            # document does not support this...
            pass

        else:
            for i in range(0, indexes.getCount()):
                indexes.getByIndex(i).update()

        try:
            document.updateLinks()

        except AttributeError:
            # documentument does not support this...
            pass

    def write_document(self, document, outfilename, filter, overwrite=False):
        outproperties = Properties(FilterName=filter)

        if overwrite:
            outproperties.add("Overwrite", True)

        out_url = self.path_to_url(outfilename)

        document.storeToURL(out_url, outproperties())

    def path_to_url(self, path):
        import uno
        return uno.systemPathToFileUrl(path)


if __name__ == '__main__':

    if len(sys.argv) < 6:
        raise OfficeException("Invalid number of arguments")

    host = sys.argv[1]
    port = sys.argv[2]
    infile = sys.argv[3]
    outfile = sys.argv[4]
    odffilter = sys.argv[5]

    ocs = OfficeClientSpawned(host, port)
    ocs.connect()
    ocs.convert(infile, outfile, odffilter)
