# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from ox import int_value


class Torrent(dict):
    '''
    >>> Torrent()
    {'files': 1, 'domain': u'', 'subtitle language': u'', 'seeder': -1, 'description': u'', 'language': u'', 'title': u'', 'imdbId': u'', 'downloaded': -1, 'leecher': -1, 'torrent_link': u'', 'torrent_info': {}, 'published': u'', 'announce': '', 'infohash': '', 'id': u'', 'comment_link': u'', 'size': -1}
    '''
    _string_keys = ('id', 'title', 'description', 'infohash', 'torrent_link', 'comment_link', 
                   'imdbId', 'announce', 'domain', 'published', 'language', 'subtitle language')
    _int_keys = ('size', 'seeder', 'leecher', 'downloaded', 'files')
    _dict_keys = ('torrent_info', )
    _list_keys = ()
    data = {'torrent_info': {}}

    def __init__(self):
        for key in self._string_keys:
            self[key] = self.data.get(key, u'')
        for key in self._dict_keys:
            self[key] = self.data.get(key, {})
        for key in self._list_keys:
            self[key] = self.data.get(key, [])
        for key in self._int_keys:
            value = self.data.get(key, -1)
            if not isinstance(value, int):
                value = int(int_value(value))
            self[key] = value
        self['infohash'] = self.data['torrent_info'].get('hash', '')
        self['size'] = self.data['torrent_info'].get('size', -1)
        self['announce'] = self.data['torrent_info'].get('announce', '')
        if 'files' in self.data['torrent_info']:
            self['files'] = len(self.data['torrent_info']['files'])
        else:
            self['files'] =  1

