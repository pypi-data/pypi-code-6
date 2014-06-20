"""Writer sending data to a cubicweb instance which store it and may be used
to display reports

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
from __future__ import with_statement
__docformat__ = "restructuredtext en"

import os
import logging
import tarfile
import tempfile
import traceback
from datetime import datetime
from StringIO import StringIO
from threading import RLock
from logilab.mtconverter import xml_escape

REVERSE_SEVERITIES = {
    logging.DEBUG :   u'DEBUG',
    logging.INFO :    u'INFO',
    logging.WARNING : u'WARNING',
    logging.ERROR :   u'ERROR',
    logging.FATAL :   u'FATAL'
    }

ARCHIVE_EXT = '.tar.bz2'
ARCHIVE_MODE = 'w:bz2'
ARCHIVE_NAME = "apycot-archive-%(instance-id)s-%(exec-id)s"+ARCHIVE_EXT
ARCHIVE_MIME_TYPE = u'application/x-tar'

def make_archive_name(cwinstid, execution_id):
    # replace ':' as tar use them to fetch archive over network
    exec_data = {'exec-id':     execution_id,
                 'instance-id': cwinstid,
                }
    return (ARCHIVE_NAME % exec_data).replace(':', '.')



class AbstractLogWriter(object):

    def _unicode(self, something):
        if isinstance(something, str):
            return unicode(something, 'utf-8', 'replace')
        if not isinstance(something, unicode):
            return unicode(something)
        return something

    def debug(self, *args, **kwargs):
        """log an debug"""
        self.log(logging.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        """log an info"""
        self.log(logging.INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        """log a warning"""
        self.log(logging.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        """log an error"""
        self.log(logging.ERROR, *args, **kwargs)

    def fatal(self, *args, **kwargs):
        """log a fatal error"""
        self.log(logging.FATAL, *args, **kwargs)

    critical = fatal

    def _msg_info(self, *args, **kwargs):
        path = kwargs.pop('path', None)
        line = kwargs.pop('line', None)
        tb = kwargs.pop('tb', False)
        assert not kwargs
        if len(args) > 1:
            args = [self._unicode(string) for string in args]
            msg = args[0] % tuple(args[1:])
        else:
            assert args
            msg = self._unicode(args[0])
        if tb:
            stream = StringIO()
            traceback.print_exc(file=stream)
            msg += '\n' + stream.getvalue()
        return path, line, msg

    def log(self, severity, *args, **kwargs):
        """log a message of a given severity"""
        path, line, msg = self._msg_info(*args, **kwargs)
        self._log(severity, path, line, msg)

    def _log(self, severity, path, line, msg):
        raise NotImplementedError()


class BaseDataWriter(AbstractLogWriter):
    """print execution message on stderr and store Test execution data to
    a CubicWeb instance (using the apycot cube)
    """

    def __init__(self, cnxh, target_url):
        self.cnxh = cnxh
        # eid of the execution entity
        self._url = target_url
        self._log_file_eid = None
        self._logs = []
        self._logs_sent = 0

    def target_eid(self):
        return self._url.rsplit('/',1)[-1]

    def instance_url(self):
        return '{0}/'.format(self._url.rsplit('/',1)[0])

    def start(self):
        pass

    def end(self):
        pass

    def set_exec_status(self, status):
        self.cnxh.http_post(self._url, vid='set_attributes', status=status)

    def execution_info(self, *args, **kwargs):
        msg = self._msg_info(*args, **kwargs)[-1]
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        print msg

    def _log(self, severity, path, line, msg):
        encodedmsg = u'%s\t%s\t%s\t%s<br/>' % (severity, xml_escape(path or u''),
                                               xml_escape(u'%s' % (line or u'')),
                                               xml_escape(msg))
        self._logs.append(encodedmsg)

    def raw(self, name, value, type=None):
        """give some raw data"""
        self.cnxh.http_post(self._url, vid='create_subentity',
                             __cwetype__='CheckResultInfo',
                             __cwrel__='for_check',
                             label=self._unicode(name),
                             value=self._unicode(value),
                             type=type and unicode(type))

    def refresh_log(self):
        log = self._logs
        if self._logs_sent < len(log):
            files = {'data': ('dummy', u''.join(log[self._logs_sent:]) )}
            if not self._log_file_eid:
                data = self.cnxh.http_post(self._url, vid='create_subentity',
                                            __cwetype__='File',
                                            __cwrel__='reverse_log_file',
                                            data_name=u'log_file.txt',
                                            data_encoding='utf-8')[0]
                self._log_file_eid = data['eid']
            self.cnxh.http_post(url=self.instance_url() + 'narval-file-append',
                                files=files,
                                eid=self._log_file_eid)

            self._logs_sent = len(log)


class CheckDataWriter(BaseDataWriter):
    """Writer intended to report Check level log and result."""

    def start(self, checker, name=None):
        """Register the given checker as started"""
        if name is not None:
            crname = name
        else:
            crname = getattr(checker, 'id', checker) # may be the checked id
        data = self.cnxh.http_post(self._url, vid='create_subentity',
                                    __cwetype__='CheckResult',
                                    __cwrel__='during_execution',
                                    name=self._unicode(crname), status=u'processing',
                                    starttime=datetime.now())
        self._url = self.cnxh.instance_url + str(data[0]['eid'])
        if hasattr(checker, 'options'):
            options = ['%s=%s' % (k, v) for k, v in checker.options.iteritems()
                       if k in checker.options_def
                       and v != checker.options_def[k].get('default')]
            if options:
                self.info('\n'.join(options))
                self.refresh_log()

    def end(self, status):
        """Register the given checker as closed with status <status>"""
        self.refresh_log()
        self.cnxh.http_post(self._url, vid='set_attributes',
                             status=self._unicode(status),
                             endtime=datetime.now(),)


class TestDataWriter(BaseDataWriter):
    """Writer intended to report Test level log and result."""

    def make_check_writer(self):
        """Return a CheckDataWriter suitable to write checker log and result within this test"""
        self.refresh_log()
        return CheckDataWriter(self.cnxh, self._url)

    def link_to_revision(self, environment, vcsrepo):
        changeset = vcsrepo.changeset()
        if changeset is not None:
            self.raw(repr(vcsrepo), changeset, 'revision')

    def start(self):
        self.set_exec_status(u'set up')

    def end(self, status, archivedir=None):
        """mark the current test as closed (with status <status>) and upload
        archive if requested."""

        self.refresh_log()
        self.cnxh.http_post(self._url, vid='set_attributes',
                            status = self._unicode(status))
        if archivedir:
            archive = make_archive_name(self.cnxh.instance_id, self.target_eid())
            archivefpath = os.path.join(tempfile.gettempdir(), archive)
            tarball = tarfile.open(archivefpath, ARCHIVE_MODE)
            try:
                tarball.add(archivedir, arcname=os.path.basename(archivedir))
                tarball.close()
                files = {'data': ('dummy', open(archivefpath, 'rb'))}
                data = self.cnxh.http_post(self._url, vid='create_subentity',
                                    __cwetype__='File',
                                    __cwrel__='reverse_execution_archive',
                                    data_name=archive,
                                    data_format=ARCHIVE_MIME_TYPE)[0]
                self.cnxh.http_post(url=self.instance_url() + 'narval-file-append', files=files, eid=data['eid'])
            except:
                self.error('while archiving execution directory', tb=True)
            finally:
                os.unlink(archivefpath)

