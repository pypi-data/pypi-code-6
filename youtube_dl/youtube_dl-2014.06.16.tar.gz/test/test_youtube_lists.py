#!/usr/bin/env python

# Allow direct execution
import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test.helper import FakeYDL


from youtube_dl.extractor import (
    YoutubeUserIE,
    YoutubePlaylistIE,
    YoutubeIE,
    YoutubeChannelIE,
    YoutubeShowIE,
    YoutubeTopListIE,
    YoutubeSearchURLIE,
)


class TestYoutubeLists(unittest.TestCase):
    def assertIsPlaylist(self, info):
        """Make sure the info has '_type' set to 'playlist'"""
        self.assertEqual(info['_type'], 'playlist')

    def test_youtube_playlist(self):
        dl = FakeYDL()
        ie = YoutubePlaylistIE(dl)
        result = ie.extract('https://www.youtube.com/playlist?list=PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re')
        self.assertIsPlaylist(result)
        self.assertEqual(result['title'], 'ytdl test PL')
        ytie_results = [YoutubeIE().extract_id(url['url']) for url in result['entries']]
        self.assertEqual(ytie_results, [ 'bV9L5Ht9LgY', 'FXxLjLQi3Fg', 'tU3Bgo5qJZE'])

    def test_youtube_playlist_noplaylist(self):
        dl = FakeYDL()
        dl.params['noplaylist'] = True
        ie = YoutubePlaylistIE(dl)
        result = ie.extract('https://www.youtube.com/watch?v=FXxLjLQi3Fg&list=PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re')
        self.assertEqual(result['_type'], 'url')
        self.assertEqual(YoutubeIE().extract_id(result['url']), 'FXxLjLQi3Fg')

    def test_issue_673(self):
        dl = FakeYDL()
        ie = YoutubePlaylistIE(dl)
        result = ie.extract('PLBB231211A4F62143')
        self.assertTrue(len(result['entries']) > 25)

    def test_youtube_playlist_long(self):
        dl = FakeYDL()
        ie = YoutubePlaylistIE(dl)
        result = ie.extract('https://www.youtube.com/playlist?list=UUBABnxM4Ar9ten8Mdjj1j0Q')
        self.assertIsPlaylist(result)
        self.assertTrue(len(result['entries']) >= 799)

    def test_youtube_playlist_with_deleted(self):
        #651
        dl = FakeYDL()
        ie = YoutubePlaylistIE(dl)
        result = ie.extract('https://www.youtube.com/playlist?list=PLwP_SiAcdui0KVebT0mU9Apz359a4ubsC')
        ytie_results = [YoutubeIE().extract_id(url['url']) for url in result['entries']]
        self.assertFalse('pElCt5oNDuI' in ytie_results)
        self.assertFalse('KdPEApIVdWM' in ytie_results)
        
    def test_youtube_playlist_empty(self):
        dl = FakeYDL()
        ie = YoutubePlaylistIE(dl)
        result = ie.extract('https://www.youtube.com/playlist?list=PLtPgu7CB4gbZDA7i_euNxn75ISqxwZPYx')
        self.assertIsPlaylist(result)
        self.assertEqual(len(result['entries']), 0)

    def test_youtube_course(self):
        dl = FakeYDL()
        ie = YoutubePlaylistIE(dl)
        # TODO find a > 100 (paginating?) videos course
        result = ie.extract('https://www.youtube.com/course?list=ECUl4u3cNGP61MdtwGTqZA0MreSaDybji8')
        entries = result['entries']
        self.assertEqual(YoutubeIE().extract_id(entries[0]['url']), 'j9WZyLZCBzs')
        self.assertEqual(len(entries), 25)
        self.assertEqual(YoutubeIE().extract_id(entries[-1]['url']), 'rYefUsYuEp0')

    def test_youtube_channel(self):
        dl = FakeYDL()
        ie = YoutubeChannelIE(dl)
        #test paginated channel
        result = ie.extract('https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w')
        self.assertTrue(len(result['entries']) > 90)
        #test autogenerated channel
        result = ie.extract('https://www.youtube.com/channel/HCtnHdj3df7iM/videos')
        self.assertTrue(len(result['entries']) >= 18)

    def test_youtube_user(self):
        dl = FakeYDL()
        ie = YoutubeUserIE(dl)
        result = ie.extract('https://www.youtube.com/user/TheLinuxFoundation')
        self.assertTrue(len(result['entries']) >= 320)

    def test_youtube_safe_search(self):
        dl = FakeYDL()
        ie = YoutubePlaylistIE(dl)
        result = ie.extract('PLtPgu7CB4gbY9oDN3drwC3cMbJggS7dKl')
        self.assertEqual(len(result['entries']), 2)

    def test_youtube_show(self):
        dl = FakeYDL()
        ie = YoutubeShowIE(dl)
        result = ie.extract('http://www.youtube.com/show/airdisasters')
        self.assertTrue(len(result) >= 3)

    def test_youtube_mix(self):
        dl = FakeYDL()
        ie = YoutubePlaylistIE(dl)
        result = ie.extract('https://www.youtube.com/watch?v=W01L70IGBgE&index=2&list=RDOQpdSVF_k_w')
        entries = result['entries']
        self.assertTrue(len(entries) >= 20)
        original_video = entries[0]
        self.assertEqual(original_video['id'], 'OQpdSVF_k_w')

    def test_youtube_toptracks(self):
        print('Skipping: The playlist page gives error 500')
        return
        dl = FakeYDL()
        ie = YoutubePlaylistIE(dl)
        result = ie.extract('https://www.youtube.com/playlist?list=MCUS')
        entries = result['entries']
        self.assertEqual(len(entries), 100)

    def test_youtube_toplist(self):
        dl = FakeYDL()
        ie = YoutubeTopListIE(dl)
        result = ie.extract('yttoplist:music:Trending')
        entries = result['entries']
        self.assertTrue(len(entries) >= 5)

    def test_youtube_search_url(self):
        dl = FakeYDL()
        ie = YoutubeSearchURLIE(dl)
        result = ie.extract('https://www.youtube.com/results?baz=bar&search_query=youtube-dl+test+video&filters=video&lclk=video')
        entries = result['entries']
        self.assertIsPlaylist(result)
        self.assertEqual(result['title'], 'youtube-dl test video')
        self.assertTrue(len(entries) >= 5)

if __name__ == '__main__':
    unittest.main()
