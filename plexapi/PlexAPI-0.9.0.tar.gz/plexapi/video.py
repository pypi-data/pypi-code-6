"""
PlexVideo
"""
from plexapi.exceptions import NotFound, UnknownType
from plexapi.utils import PlexPartialObject, NA
from plexapi.utils import cast, toDatetime


class Video(PlexPartialObject):
    TYPE = None

    def __eq__(self, other):
        return self.type == other.type and self.key == other.key

    def __repr__(self):
        clsname = self.__class__.__name__
        title = self.title.replace(' ','.')[0:20]
        return '<%s:%s>' % (clsname, title)

    def _loadData(self, data):
        self.type = data.attrib.get('type', NA)
        self.key = data.attrib.get('key', NA)
        self.ratingKey = data.attrib.get('ratingKey', NA)
        self.title = data.attrib.get('title', NA)
        self.summary = data.attrib.get('summary', NA)
        self.art = data.attrib.get('art', NA)
        self.thumb = data.attrib.get('thumb', NA)
        self.addedAt = toDatetime(data.attrib.get('addedAt', NA))
        self.updatedAt = toDatetime(data.attrib.get('updatedAt', NA))
        self.lastViewedAt = toDatetime(data.attrib.get('lastViewedAt', NA))

    def analyze(self):
        self.server.query('/%s/analyze' % self.key)

    def markWatched(self):
        path = '/:/scrobble?key=%s&identifier=com.plexapp.plugins.library' % self.ratingKey
        self.server.query(path)
        self.reload()

    def markUnwatched(self):
        path = '/:/unscrobble?key=%s&identifier=com.plexapp.plugins.library' % self.ratingKey
        self.server.query(path)
        self.reload()

    def play(self, client):
        client.playMedia(self)

    def refresh(self):
        self.server.query('/%s/refresh' % self.key)


class Movie(Video):
    TYPE = 'movie'

    def _loadData(self, data):
        super(Movie, self)._loadData(data)
        self.studio = data.attrib.get('studio', NA)
        self.contentRating = data.attrib.get('contentRating', NA)
        self.rating = data.attrib.get('rating', NA)
        self.viewCount = cast(int, data.attrib.get('viewCount', 0))
        self.year = cast(int, data.attrib.get('year', NA))
        self.tagline = data.attrib.get('tagline', NA)
        self.duration = cast(int, data.attrib.get('duration', NA))
        self.originallyAvailableAt = toDatetime(data.attrib.get('originallyAvailableAt', NA), '%Y-%m-%d')
        self.primaryExtraKey = data.attrib.get('primaryExtraKey', NA)


class Show(Video):
    TYPE = 'show'
        
    def _loadData(self, data):
        super(Show, self)._loadData(data)
        self.studio = data.attrib.get('studio', NA)
        self.contentRating = data.attrib.get('contentRating', NA)
        self.rating = data.attrib.get('rating', NA)
        self.year = cast(int, data.attrib.get('year', NA))
        self.banner = data.attrib.get('banner', NA)
        self.theme = data.attrib.get('theme', NA)
        self.duration = cast(int, data.attrib.get('duration', NA))
        self.originallyAvailableAt = toDatetime(data.attrib.get('originallyAvailableAt', NA), '%Y-%m-%d')
        self.leafCount = cast(int, data.attrib.get('leafCount', NA))
        self.viewedLeafCount = cast(int, data.attrib.get('viewedLeafCount', NA))
        self.childCount = cast(int, data.attrib.get('childCount', NA))

    def seasons(self):
        path = '/library/metadata/%s/children' % self.ratingKey
        return list_items(self.server, path, Season.TYPE)

    def season(self, title):
        path = '/library/metadata/%s/children' % self.ratingKey
        return find_item(self.server, path, title)

    def episodes(self):
        leavesKey = '/library/metadata/%s/allLeaves' % self.ratingKey
        return list_items(self.server, leavesKey)

    def episode(self, title):
        path = '/library/metadata/%s/allLeaves' % self.ratingKey
        return find_item(self.server, path, title)

    def find(self, title):
        return self.episode(title)


class Season(Video):
    TYPE = 'season'

    def _loadData(self, data):
        super(Season, self)._loadData(data)
        self.librarySectionID = data.attrib.get('librarySectionID', NA)
        self.librarySectionTitle = data.attrib.get('librarySectionTitle', NA)
        self.parentRatingKey = data.attrib.get('parentRatingKey', NA)
        self.parentKey = data.attrib.get('parentKey', NA)
        self.parentTitle = data.attrib.get('parentTitle', NA)
        self.parentSummary = data.attrib.get('parentSummary', NA)
        self.index = data.attrib.get('index', NA)
        self.parentIndex = data.attrib.get('parentIndex', NA)
        self.parentThumb = data.attrib.get('parentThumb', NA)
        self.parentTheme = data.attrib.get('parentTheme', NA)
        self.leafCount = cast(int, data.attrib.get('leafCount', NA))
        self.viewedLeafCount = cast(int, data.attrib.get('viewedLeafCount', NA))

    def episodes(self):
        childrenKey = '/library/metadata/%s/children' % self.ratingKey
        return list_items(self.server, childrenKey)

    def show(self):
        return list_items(self.server, self.parentKey)[0]


class Episode(Video):
    TYPE = 'episode'

    def _loadData(self, data):
        super(Episode, self)._loadData(data)
        self.librarySectionID = data.attrib.get('librarySectionID', NA)
        self.librarySectionTitle = data.attrib.get('librarySectionTitle', NA)
        self.grandparentKey = data.attrib.get('grandparentKey', NA)
        self.grandparentTitle = data.attrib.get('grandparentTitle', NA)
        self.grandparentThumb = data.attrib.get('grandparentThumb', NA)
        self.parentKey = data.attrib.get('parentKey', NA)
        self.parentIndex = data.attrib.get('parentIndex', NA)
        self.parentThumb = data.attrib.get('parentThumb', NA)
        self.contentRating = data.attrib.get('contentRating', NA)
        self.index = data.attrib.get('index', NA)
        self.rating = data.attrib.get('rating', NA)
        self.viewCount = cast(int, data.attrib.get('viewCount', 0))
        self.year = cast(int, data.attrib.get('year', NA))
        self.duration = cast(int, data.attrib.get('duration', NA))
        self.originallyAvailableAt = toDatetime(data.attrib.get('originallyAvailableAt', NA), '%Y-%m-%d')

    def season(self):
        return list_items(self.server, self.parentKey)[0]

    def show(self):
        return list_items(self.server, self.grandparentKey)[0]


class Media:
    
    def __init__(self, server, data):
        self.videoResolution = self.data.attrib.get('videoResolution')
        self.id = self.data.attrib.get('id')
        self.duration = self.data.attrib.get('duration')
        self.bitrate = self.data.attrib.get('bitrate')
        self.width = self.data.attrib.get('width')
        self.height = self.data.attrib.get('height')
        self.aspectRatio = self.data.attrib.get('aspectRatio')
        self.audioChannels = self.data.attrib.get('audioChannels')
        self.audioCodec = self.data.attrib.get('audioCodec')
        self.videoCodec = self.data.attrib.get('videoCodec')
        self.container = self.data.attrib.get('container')
        self.videoFrameRate = self.data.attrib.get('videoFrameRate')


class MediaPart:

    def __init__(self, server, data):
        self.id = self.data.attrib.get('id')
        self.key = self.data.attrib.get('key')
        self.duration = self.data.attrib.get('duration')
        self.file = self.data.attrib.get('file')
        self.size = self.data.attrib.get('size')
        self.container = self.data.attrib.get('container')


def build_item(server, elem, initpath):
    VIDEOCLS = {Movie.TYPE:Movie, Show.TYPE:Show, Season.TYPE:Season, Episode.TYPE:Episode}
    vtype = elem.attrib.get('type')
    if vtype in VIDEOCLS:
        cls = VIDEOCLS[vtype]
        return cls(server, elem, initpath)
    raise UnknownType('Unknown video type: %s' % vtype)


def find_item(server, path, title):
    for elem in server.query(path):
        if elem.attrib.get('title') == title:
            return build_item(server, elem, path)
    raise NotFound('Unable to find title: %s' % title)


def list_items(server, path, videotype=None):
    items = []
    for elem in server.query(path):
        if not videotype or elem.attrib.get('type') == videotype:
            try:
                items.append(build_item(server, elem, path))
            except UnknownType:
                pass
    return items


def search_type(videotype):
    if videotype == Movie.TYPE: return 1
    elif videotype == Show.TYPE: return 2
    elif videotype == Season.TYPE: return 3
    elif videotype == Episode.TYPE: return 4
    raise NotFound('Unknown videotype: %s' % videotype)
