from ftw.downloadtoken.interfaces import IDownloadlinkOpened
from ftw.downloadtoken.interfaces import IDownloadlinkSent
from zope.interface import implements


class DownloadlinkSent(object):
    """Event for journal entries"""
    implements(IDownloadlinkSent)

    def __init__(self, obj, email, comment):
        self.obj = obj
        self.emails = email
        self.comment = comment


class DownloadlinkOpened(object):
    """Event for journal entries"""
    implements(IDownloadlinkOpened)

    def __init__(self, obj, email):
        self.obj = obj
        self.email = email
