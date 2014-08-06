# future imports
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# stdlib imports
import os
import unittest

# local imports
from radiobabel import SoundcloudClient
from radiobabel.errors import TrackNotFound
from radiobabel.test_utils import load_config


class ClientInitializationTests(unittest.TestCase):

    def test_no_client_id(self):
        """Test that proper error is raised when no client id is provided
        """
        with self.assertRaises(TypeError):
            SoundcloudClient()

    def test_client_id_passed_in(self):
        """Soundcloud: Client ID is correctly read from passed-in args
        """
        try:
            SoundcloudClient('XXXX')
        except:
            self.fail("Exception unexpectedly raised")


class LookupTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = SoundcloudClient(os.environ['SOUNDCLOUD_CLIENT_ID'])

    def test_valid_lookup_str(self):
        """Soundcloud: Looking up a valid track (str) returns the expected data
        """
        track = self.client.track('18048610')
        self.assertDictEqual(track, {
            'album': None,
            'artists': [
                {
                    'name': 'WUGAZI',
                    'source_type': 'soundcloud',
                    'source_id': 5613872,
                },
            ],
            'track_number': 0,
            'source_id': 18048610,
            'name': 'Sleep Rules Everything Around Me',
            'duration_ms': 199180,
            'preview_url': 'https://api.soundcloud.com/tracks/18048610/stream',
            'source_type': 'soundcloud',
            'image_url': 'https://i1.sndcdn.com/artworks-000008722839-oyzy1n-large.jpg?e76cf77',
        })

    def test_valid_lookup_int(self):
        """Soundcloud: Looking up a valid track (str) returns the expected data
        """
        track = self.client.track(18048610)
        self.assertDictEqual(track, {
            'album': None,
            'artists': [
                {
                    'name': 'WUGAZI',
                    'source_type': 'soundcloud',
                    'source_id': 5613872,
                },
            ],
            'track_number': 0,
            'source_id': 18048610,
            'name': 'Sleep Rules Everything Around Me',
            'duration_ms': 199180,
            'preview_url': 'https://api.soundcloud.com/tracks/18048610/stream',
            'source_type': 'soundcloud',
            'image_url': 'https://i1.sndcdn.com/artworks-000008722839-oyzy1n-large.jpg?e76cf77',
        })

    def test_invalid_lookup(self):
        """Soundcloud: Looking up an invalid track raises the appropriate error
        """
        with self.assertRaises(TrackNotFound):
            self.client.track('asfasfasfas')


class SearchTests(unittest.TestCase):

    def setUp(self):
        load_config()
        self.client = SoundcloudClient(os.environ['SOUNDCLOUD_CLIENT_ID'])

    def test_search_returns_results(self):
        """Soundcloud: Test that search results are returned in the correct format
        """
        results = self.client.search('wugazi')
        self.assertGreater(len(results), 0)
