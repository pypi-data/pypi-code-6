from lacore.adf.elements import Links
from lacore.archive.urls import UrlArchiver
from . import Dumper


class UrlDumper(Dumper, UrlArchiver):

    def __init__(self, **kwargs):
        super(UrlDumper, self).__init__(**kwargs)

    def update(self, result):
        super(UrlDumper, self).update(result)
        self.docs['links'] = Links()

    def write(self, data):
        print "dummy writing", len(data)
