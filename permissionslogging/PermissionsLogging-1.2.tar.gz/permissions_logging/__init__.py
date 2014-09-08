"""
A collection of log handlers that allow file permissions to be specified.
"""
import logging
import logging.handlers as handlers
import os
import datetime

class FileHandler(logging.FileHandler):
    """
    A subclass of logging.FileHandler that accepts a permissions argument.

    The file used for logging will have the value of the permissions keyword
    value, e.g. for unix:  permissions=0o664
    """
    def __init__(self, filename, permissions=0o644, **kwargs):
        self.permissions = permissions
        logging.FileHandler.__init__(self, filename)

    def _open(self):
        stream = logging.FileHandler._open(self)
        try:
            os.chmod(self.baseFilename, self.permissions)
        except OSError as ex:
            # If we don't have access to change the permissions, we need to
            # rely on the initial file creator having done the chmod
            pass

        return stream


class DateNameFileHandler(FileHandler):
    """
    A subclass that allows for filenames w/ a dateformat.
    Will close and reopen filehandles as needed.
    For example, you could configure a handler to to have this filename:
    /tmp/logs/my_app-%Y-%M-%d.log
    """
    def __init__(self, *args, **kwargs):
        self._originalBaseFilename = None
        FileHandler.__init__(self, *args, **kwargs)

    def emit(self, *args, **kwargs):
        """
        If we our open file's name no longer matches the current moment's
        version of the filename, close it.  emit in FileHandler will open
        a new handle as needed.
        """
        if self.baseFilename != self._get_current_filename():
            self.close()

        FileHandler.emit(self, *args, **kwargs)

    def _open(self, *args, **kwargs):
        """
        Saves the original base filename, then overrides it with a date
        formatted filename.  Uses strftime arguments.
        """
        if not self._originalBaseFilename:
            self._originalBaseFilename = self.baseFilename

        self.baseFilename = self._get_current_filename()

        return FileHandler._open(self, *args, **kwargs)

    def _get_current_filename(self):
        return datetime.datetime.now().strftime(self._originalBaseFilename)


class TimedRotatingFileHandler(FileHandler, handlers.TimedRotatingFileHandler):
    """
    A subclass of logging.handlers.TimedRotatingFileHandler that accepts
    a permissions argument.

    The file used for logging will have the value of the permissions keyword
    value, e.g. for unix:  permissions=0o664
    """
    def __init__(self, filename, permissions=0o644, **kwargs):
        self.permissions = permissions
        handlers.TimedRotatingFileHandler.__init__(self, filename, **kwargs)


class WatchedFileHandler(FileHandler, handlers.WatchedFileHandler):
    """
    A subclass of logging.handlers.WatchedFileHandler that accepts
    a permissions argument.

    The file used for logging will have the value of the permissions keyword
    value, e.g. for unix:  permissions=0o664
    """
    def __init__(self, filename, permissions=0o644, **kwargs):
        self.permissions = permissions
        handlers.WatchedFileHandler.__init__(self, filename, **kwargs)


class RotatingFileHandler(FileHandler, handlers.RotatingFileHandler):
    """
    A subclass of logging.handlers.RotatingFileHandler that accepts
    a permissions argument.

    The file used for logging will have the value of the permissions keyword
    value, e.g. for unix:  permissions=0o664
    """
    def __init__(self, filename, permissions=0o644, **kwargs):
        self.permissions = permissions
        handlers.RotatingFileHandler.__init__(self, filename, **kwargs)
