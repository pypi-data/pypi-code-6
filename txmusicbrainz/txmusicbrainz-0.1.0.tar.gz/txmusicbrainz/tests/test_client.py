from unittest import TestCase

from txmusicbrainz.client import MusicBrainz


class TestMusicBrainzInit(TestCase):
    def test_user_agent(self):
        client = MusicBrainz(
            app_name="test",
            app_version="0.1.0",
            contact_info="me@example.com",
        )
        self.assertEqual(client.user_agent, "test/0.1.0 (me@example.com)")
