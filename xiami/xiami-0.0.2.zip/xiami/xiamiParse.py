# -*- coding: utf-8 -*-

__author__ = 'rsj217'

import urllib2


class XiamiParser(object):


    @classmethod
    def get_song_info(cls, data):
        """ 获取歌曲的信息
        Args:
            :param data: 请求访问返回的数据信息
        Return:
            歌曲的信息，包含标题，专辑名称，歌词地址，歌曲地址
        """

        # print cls
        # return

        trackList = data['data']['trackList'][0]
        song_info = {
            'song_id': trackList['song_id'],
            'title': trackList['title'],
            'pic': trackList['pic'],
            'lyric': trackList['lyric'],
            'song_url': cls._get_song_url(cls._caser_code(trackList['location']))
        }
        return song_info

    @classmethod
    def _caser_code(cls, ciphertext=''):
        """ 凯撒加密的解密方法
        Args:
            :param  ciphertext: 已经加密的字符串
        Return：
            解密之后的字符串
        """
        cipher_len = len(ciphertext) - 1
        rows = int(ciphertext[0])
        cols, offset_rows = cipher_len / rows , cipher_len % rows
        text = ciphertext[1:]
        plaintext = ''
        for i in xrange(cipher_len):
            x = i % rows
            y = i / rows
            p = 0
            if x <= offset_rows:
                p = x * (cols + 1) + y
            else:
                p = offset_rows * (cols + 1) + (x - offset_rows) * cols + y
            plaintext += text[p]
        return plaintext

    @classmethod
    def _get_song_url(cls, orgin_url):
        """ 获取歌曲的真实url地址
        Args：
            :param orgin_url: 解密之后的url字符串，原始的url地址
        """
        mp3_url = urllib2.unquote(orgin_url).replace('^', '0')
        return mp3_url

if __name__ == '__main__':
    d = {
        'status': True,
        'jumpurl': None,
        'message': u'',
        'data': {
            'hqset': 0,
            'type_id': 1,
            'trackList': [{
                              'lyric_url': u'http://www.xiami.com/lyric/1/1773346501_14056804704181.lrc',
                              'album_id': u'1602302708',
                              'grade': -1,
                              'pic': u'http://img.xiami.net/images/album/img78/778/16023027081405476412_1.jpg',
                              'lyric': u'http://img.xiami.net/lyric/1/1773346501_14056804704181.lrc',
                              'rec_note': u'', u'insert_type': 1,
                              'title': u'\u5e73\u51e1\u4e4b\u8def',
                              'aritst_type': u'',
                              'object_id': u'1773346501',
                              'album_pic': u'http://img.xiami.net/images/album/img78/778/16023027081405476412.jpg',
                              'object_name': u'default',
                              'location': u'9hFlc%1EF%63kadd19Elt%eo262156%ea1188-t2.mF%77E93y27b-7%pFx%75%714F%ef8125%mi27E53__a37814%E35aF82E31luDd33%5-A.m7%3845.t8dff5En%fi72%%65mhbbd2E%u2i.8F5256p_696755l',
                              'artist_id': u'778',
                              'background': u'http://img.xiami.net/res/player/bimg/bg-5.jpg',
                              'album_name': u'\u5e73\u51e1\u4e4b\u8def',
                              'song_id': u'1773346501',
                              'artist': u'\u6734\u6811',
                              'tryhq': 0,
                              'length': 302,
                              'artist_url': u'http://www.xiami.com/artist/778', u'ms': None}],
            'vip_role': 0,
            'lastSongId': 0,
            'vip': 0,
            'clearlist': None,
            'type': u'default'}}

    location = d['data']['trackList'][0]['location']

    print XiamiParser.get_song_info(d)