# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import soundcloud

# local imports
from radiobabel.errors import TrackNotFound


logger = logging.getLogger('radiobabel.backends.soundcloud')


def _transform_track(track):
    """Transform result into a format that more closely matches our unified API.
    """
    transformed_track = dict([
        ('source_type', 'soundcloud'),
        ('source_id', track['id']),
        ('name', track['title']),
        ('duration_ms', track['duration']),
        ('preview_url', track.get('stream_url')),
        ('track_number', 0),
    ])
    transformed_track['artists'] = [
        dict([
            ('source_type', 'soundcloud'),
            ('source_id', track['user']['id']),
            ('name', track['user']['username']),
        ]),
    ]
    transformed_track['album'] = None
    if track['artwork_url']:
        transformed_track['image_url'] = track['artwork_url']
    else:
        transformed_track['image_url'] = 'http://judejohnstone.com/wp-content/themes/soundcheck/images/default-artwork.png'
    return transformed_track


class SoundcloudClient(object):

    def __init__(self, client_id):
        """Initialise soundcloud API client.
        """
        self.client = soundcloud.Client(client_id=client_id)

    def track(self, track_id):
        """Lookup a single track using the soundcloud API
        """
        logger.info('Track lookup: {0}'.format(track_id))

        try:
            track = self.client.get('/tracks', ids=track_id)[0].obj
        except IndexError:
            raise TrackNotFound('Soundcloud: {0}'.format(track_id))
        return _transform_track(track)

    def search(self, query, limit=200, offset=0):
        """Search for tracks using the soundcloud API
        """
        logger.info('Searching: Limit {0}, Offset {1}'.format(limit, offset))

        tracks = self.client.get('/tracks', q=query, limit=limit, offset=offset)
        return [_transform_track(x.obj) for x in tracks]
