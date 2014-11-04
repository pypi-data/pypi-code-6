"""
PlexAPI Media
"""
from plexapi.utils import cast


class Media(object):
    TYPE = 'Media'
    
    def __init__(self, server, data, initpath, video):
        self.server = server
        self.initpath = initpath
        self.video = video
        self.videoResolution = data.attrib.get('videoResolution')
        self.id = cast(int, data.attrib.get('id'))
        self.duration = cast(int, data.attrib.get('duration'))
        self.bitrate = cast(int, data.attrib.get('bitrate'))
        self.width = cast(int, data.attrib.get('width'))
        self.height = cast(int, data.attrib.get('height'))
        self.aspectRatio = cast(float, data.attrib.get('aspectRatio'))
        self.audioChannels = cast(int, data.attrib.get('audioChannels'))
        self.audioCodec = data.attrib.get('audioCodec')
        self.videoCodec = data.attrib.get('videoCodec')
        self.container = data.attrib.get('container')
        self.videoFrameRate = data.attrib.get('videoFrameRate')
        self.optimizedForStreaming = cast(bool, data.attrib.get('optimizedForStreaming'))
        self.optimizedForStreaming = cast(bool, data.attrib.get('has64bitOffsets'))
        self.parts = [MediaPart(server, elem, initpath, self) for elem in data]

    def __repr__(self):
        clsname = self.__class__.__name__
        title = self.video.title.replace(' ','.')[0:20]
        return '<%s:%s>' % (clsname, title)


class MediaPart(object):
    TYPE = 'Part'

    def __init__(self, server, data, initpath, media):
        self.server = server
        self.initpath = initpath
        self.media = media
        self.id = cast(int, data.attrib.get('id'))
        self.key = data.attrib.get('key')
        self.duration = cast(int, data.attrib.get('duration'))
        self.file = data.attrib.get('file')
        self.size = cast(int, data.attrib.get('size'))
        self.container = data.attrib.get('container')

    def __repr__(self):
        clsname = self.__class__.__name__
        return '<%s:%s>' % (clsname, self.id)


class VideoTag(object):
    TYPE = None

    def __init__(self, server, data):
        self.server = server
        self.id = cast(int, data.attrib.get('id'))
        self.tag = data.attrib.get('tag')
        self.role = data.attrib.get('role')

    def __repr__(self):
        clsname = self.__class__.__name__
        tag = self.tag.replace(' ','.')[0:20]
        return '<%s:%s:%s>' % (clsname, self.id, tag)

    def related(self, vtype=None):
        return self.server.library.search(None, **{self.FILTER:self})


class Country(VideoTag): TYPE='Country'; FILTER='country'
class Director(VideoTag): TYPE = 'Director'; FILTER='director'
class Genre(VideoTag): TYPE='Genre'; FILTER='genre'
class Producer(VideoTag): TYPE = 'Producer'; FILTER='producer'
class Actor(VideoTag): TYPE = 'Role'; FILTER='actor'
class Writer(VideoTag): TYPE = 'Writer'; FILTER='writer'
