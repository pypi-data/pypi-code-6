# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2007-2012

from threading import Event
from hashlib import sha1
import os
from six import PY2

if PY2:
    from .bencode import bencode, bdecode
else:
    from .bencode3 import bencode, bdecode

__all__ = ['create_torrent', 'get_info_hash', 'get_torrent_info', 'get_files', 'get_torrent_size']

def create_torrent(file, url, params = {}, flag = Event(),
                   progress = lambda x: None, progress_percent = 1):
    "Creates a torrent for a given file, using url as tracker url"
    from .makemetafile import make_meta_file
    return make_meta_file(file, url, params, flag, progress, progress_percent)

def get_info_hash(torrentFile):
    "Returns Torrent Info Hash from torrent file"
    metainfo_file = open(torrentFile, 'rb')
    metainfo = bdecode(metainfo_file.read())
    info = metainfo['info']
    return sha1(bencode(info)).hexdigest()

def get_torrent_info(data=None, file=None):
    if file:
        if not isinstance(file, bytes):
            file = file.encode('utf-8')
        with open(file, 'rb') as f:
            data = f.read()

    "Returns Torrent Info from torrent file"
    tinfo = {}
    metainfo = bdecode(data)
    info = metainfo['info']
    piece_length = info['piece length']
    if 'length' in info:
        # let's assume we just have one file
        file_length = info['length']
    else:
        # let's assume we have a directory structure
        file_length = 0;
        for f in info['files']:
            file_length += f['length']
    for key in info:
        if key != 'pieces':
            tinfo[key] = info[key]
    for key in metainfo:
        if key != 'info':
            tinfo[key] = metainfo[key]
    tinfo['size'] = file_length
    tinfo['hash'] = sha1(bencode(info)).hexdigest()
    tinfo['announce'] = metainfo['announce']
    if file:
        tinfo['timestamp'] = os.stat(file).st_ctime
    return tinfo

def get_files(data):
    files = []
    info = get_torrent_info(data=data)
    if 'files' in info:
        for f in info['files']:
            path = [info['name'], ]
            path.extend(f['path'])
            files.append(os.path.join(*path))
    else:
        files.append(info['name'])
    return files

def get_torrent_size(file):
    "Returns Size of files in torrent file in bytes"
    return get_torrent_info(file=file)['size']

