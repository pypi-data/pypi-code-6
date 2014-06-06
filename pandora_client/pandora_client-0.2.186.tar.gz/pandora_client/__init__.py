#!/usr/bin/python
# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2012
from __future__ import division, with_statement

import getpass
from glob import glob
import imp
import json
import math
import os
import shutil
import socket
import sqlite3
import sys
import time
import pkg_resources
from urlparse import urlparse

import ox

import extract
import utils


DEBUG = False

__version__ = pkg_resources.require("pandora_client")[0].version

socket.setdefaulttimeout(300)
CHUNK_SIZE = 1024*1024
default_media_cache = os.environ.get('oxMEDIA', '~/.ox/media')

def get_frames(filename, prefix, info, force=False):
    oshash = info['oshash']
    cache = os.path.join(prefix, os.path.join(*utils.hash_prefix(oshash)))
    frames = []
    for pos in utils.video_frame_positions(info['duration']):
        frame_name = '%s.png' % pos
        frame_f = os.path.join(cache, frame_name)
        if force or not os.path.exists(frame_f):
            print frame_f
            extract.frame(filename, frame_f, pos)
        frames.append(frame_f)
    return frames

def encode(filename, prefix, profile, info=None, extract_frames=True):
    if not info:
        info = utils.avinfo(filename)
    if not 'oshash' in info:
        return None
    oshash = info['oshash']
    cache = os.path.join(prefix, os.path.join(*utils.hash_prefix(oshash)))
    if info.get('video') and extract_frames:
        frames = get_frames(filename, prefix, info)
    else:
        frames = []
    if info.get('video') or info.get('audio'):
        media_f = os.path.join(cache, profile)
        if not os.path.exists(media_f) \
            or os.stat(media_f).st_size == 0:
            extract.video(filename, media_f, profile, info)
    else:
        print info
        print filename
        return None
    return {
        'info': info,
        'oshash': oshash,
        'frames': frames,
        'media': media_f
    }

def encode_cmd(filename, prefix, profile, info):
    if not info:
        info = utils.avinfo(filename)
    if not 'oshash' in info:
        return None
    oshash = info['oshash']
    cache = os.path.join(prefix, os.path.join(*utils.hash_prefix(oshash)))
    media_f = os.path.join(cache, profile)
    return extract.video_cmd(filename, media_f, profile, info)

def parse_path(client, path):
    '''
        args:
            path   - path without volume prefix 
            client - Client instance
        return:
            return None if file will not be used, dict with parsed item information otherwise
    '''
    if len(path.split('/')) != client.folderdepth:
        return None
    info = ox.movie.parse_path(path)
    if client.folderdepth == 3:
        info['director'] = []
        info['directorSort'] = []
    return info

def example_path(client):
    return '\t' + (client.folderdepth == 4 and 'L/Last, First/Title (Year)/Title.avi' or 'T/Title/Title.dv')

def ignore_file(client, path):
    filename = os.path.basename(path)
    if filename.startswith('._') \
        or filename in ('.DS_Store', 'Thumbs.db') \
        or filename.endswith('~') \
        or 'Extras/' in path \
        or 'Versions/' in path \
        or not os.path.exists(path) \
        or os.stat(path).st_size == 0:
        return True
    return False

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

class Client(object):
    _configfile = None

    def __init__(self, config, offline=False):
        if isinstance(config, basestring):
            self._configfile = os.path.expanduser(config)
            with open(config) as f:
                try:
                    self._config = json.load(f)
                except ValueError:
                    print "Failed to parse config at", config
                    sys.exit(1)
            base = self._config.get('plugin.d', '~/.ox/client.d')
            self.load_plugins(base)
        else:
            self._config = config
        if not self._config['url'].endswith('/'):
            self._config['url'] = self._config['url'] + '/'
        self.resolutions = list(reversed(sorted(self._config.get('resolutions', [480]))))
        self.format = self._config.get('format', 'webm')
        self.importFrames = False

        if not offline:
            self.online()

        conn, c = self._conn()

        c.execute(u'CREATE TABLE IF NOT EXISTS setting (key varchar(1024) unique, value text)')

        if int(self.get('version', 0)) < 1:
            self.set('version', 1)
            db = [
                u'''CREATE TABLE IF NOT EXISTS file (
                                path varchar(1024) unique,
                                oshash varchar(16),
                                atime FLOAT,
                                ctime FLOAT,
                                mtime FLOAT,
                                size INT,
                                info TEXT,
                                created INT,
                                modified INT,
                                deleted INT)''',
                u'CREATE INDEX IF NOT EXISTS path_idx ON file (path)',
                u'CREATE INDEX IF NOT EXISTS oshash_idx ON file (oshash)',
            ]
            for i in db:
                c.execute(i)
            conn.commit()
        if int(self.get('version', 0)) < 2:
            self.set('version', 2)
            db = [
                u'''CREATE TABLE IF NOT EXISTS encode (
                                oshash varchar(16),
                                site varchar(255))''',
                u'CREATE INDEX IF NOT EXISTS upload_site_idx ON encode (site)',
            ]
            for i in db:
                c.execute(i)
            conn.commit()
        if int(self.get('version', 0)) < 3:
            self.set('version', 3)
            db = [
                u'ALTER TABLE file add sha1 varchar(42)'
            ]
            for i in db:
                c.execute(i)
            conn.commit()
        if int(self.get('version', 0)) < 4:
            self.set('version', 4)
            db = [
                u'ALTER TABLE encode add status varchar(255)',
                u'CREATE INDEX IF NOT EXISTS encode_status_idx ON encode (status)',
                u'ALTER TABLE encode ADD modified INT DEFAULT 0',
            ]
            for i in db:
                c.execute(i)
            conn.commit()

    def load_plugins(self, base='~/.ox/client.d'):
        global parse_path, example_path, ignore_file, encode
        base = os.path.expanduser(base)
        for path in sorted(glob('%s/*.py' % base)):
            with open(path) as fp:
                module = imp.load_source(os.path.basename(path).split('.')[0], base, fp)
                if hasattr(module, 'parse_path'):
                    parse_path = module.parse_path
                if hasattr(module, 'example_path'):
                    example_path = module.example_path
                if hasattr(module, 'ignore_file'):
                    ignore_file = module.ignore_file
                if hasattr(module, 'encode'):
                    encode = module.encode

    def _conn(self):
        db_conn = os.path.expanduser(self._config['cache'])
        if not os.path.exists(os.path.dirname(db_conn)):
            os.makedirs(os.path.dirname(db_conn))
        conn = sqlite3.connect(db_conn, timeout=10)
        return conn, conn.cursor()

    def media_cache(self):
        return os.path.expanduser(self._config.get('media-cache', default_media_cache))
    
    def get(self, key, default=None):
        conn, c = self._conn()
        c.execute(u'SELECT value FROM setting WHERE key = ?', (key, ))
        for row in c:
            return row[0]
        return default

    def set(self, key, value):
        conn, c = self._conn()
        c.execute(u'INSERT OR REPLACE INTO setting values (?, ?)', (key, str(value)))
        conn.commit()

    def info(self, oshash):
        conn, c = self._conn()
        c.execute(u'SELECT info FROM file WHERE oshash = ?', (oshash, ))
        info = None
        for row in c:
            info = json.loads(row[0])
            break
        return info

    def get_info(self, oshash, prefix=None):
        if prefix:
            prefixes = [prefix]
        else:
            prefixes = self.active_volumes().values()
        prefixes = [p.decode('utf-8') if isinstance(prefix, str) else p for p in prefixes]
        _info = self.info(oshash)
        for path in self.path(oshash):
            for prefix in prefixes:
                if path.startswith(prefix) and os.path.exists(path):
                    path = path[len(prefix):]
                    i = parse_path(self, path)
                    if i:
                        _info.update(i)
                        return _info
                    else:
                        print 'failed to parse', path
                        return

    def get_info_for_ids(self, ids, prefix=None):
        info = {}
        for oshash in ids:
            i = self.get_info(oshash, prefix)
            if i:
                info[oshash] = i
        return info

    def path(self, oshash):
        conn, c = self._conn()
        c.execute(u'SELECT path FROM file WHERE oshash = ?', (oshash, ))
        paths = []
        for row in c:
            path = row[0]
            paths.append(path)
        return paths

    def online(self):
        self.api = API(self._config['url'], media_cache=self.media_cache())
        self.api.DEBUG = DEBUG
        if self.signin():
            self.resolutions = list(reversed(sorted(self.api.site['video']['resolutions'])))
            self.format = self.api.site['video']['formats'][0]
            self.importFrames = self.api.site['media'].get('importFrames')
        self.folderdepth = self._config.get('folderdepth', self.api.site['site'].get('folderdepth', 3))

    def signin(self):
        if 'username' in self._config:
            r = self.api.signin(username=self._config['username'], password=self._config['password'])
            if r['status']['code'] == 200 and not 'errors' in r['data']:
                self.user = r['data']['user']
            else:
                self.user = False
                if DEBUG:
                    print r
                print '\nlogin failed! check config\n\n'
                sys.exit(1)
            r = self.api.init()
            if r['status']['code'] == 200:
                self.api.site = r['data']['site']
            else:
                print "\n init failed.", r['status']
                sys.exit(1)
            return True

    def set_encodes(self, site, files):
        conn, c = self._conn()
        c.execute(u'DELETE FROM encode WHERE site = ?' , (site, ))
        conn.commit()
        self.add_encodes(site, files)

    def get_encodes(self, site, status=''):
        conn, c = self._conn()
        sql = u'SELECT oshash FROM encode WHERE site = ? AND status = ?'
        args = [site, status]
        c.execute(sql, tuple(args))
        return [row[0] for row in c]

    def add_encodes(self, site, files):
        conn, c = self._conn()
        for oshash in files:
            c.execute(u'INSERT INTO encode VALUES (?, ?, ?, 0)', (oshash, site, ''))
        conn.commit()

    def update_encodes(self, add=False):
        #send empty list to get updated list of requested info/files/data
        site = self._config['url']
        post = {'info': {}}
        r = self.api.update(post)
        files = r['data']['data']
        if add:
            conn, c = self._conn()
            sql = u'SELECT oshash FROM encode WHERE site = ?'
            c.execute(sql, (site, ))
            known = [row[0] for row in c]
            files = list(set(files) - set(known))
            self.add_encodes(site, files)
        else:
            self.set_encodes(site, files)

    def scan_file(self, path, rescan=False):
        conn, c = self._conn()

        update = True
        modified = time.mktime(time.localtime())
        created = modified

        if isinstance(path, str):
            path = path.decode('utf-8')

        sql = u'SELECT atime, ctime, mtime, size, created, info FROM file WHERE deleted < 0 AND path=?'
        c.execute(sql, [path])
        stat = os.stat(path)
        for row in c:
            if stat.st_atime == row[0] and stat.st_ctime == row[1] and stat.st_mtime == row[2] and stat.st_size == row[3]:
                created = row[4]
                info = json.loads(row[5])
                update = False
            break
        if update or rescan:
            info = utils.avinfo(path, cached=not rescan)
            if info['size'] > 0:
                oshash = info['oshash']
                sha1 = None
                deleted = -1
                t = (path, oshash, stat.st_atime, stat.st_ctime, stat.st_mtime,
                     stat.st_size, json.dumps(info), created, modified, deleted, sha1)
                c.execute(u'INSERT OR REPLACE INTO file values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          t)
                conn.commit()
        return 'error' not in info

    def get_resolution(self, info):
        height = info['video'][0]['height'] if info.get('video') else None
        for resolution in sorted(self.resolutions):
            if height and height <= resolution:
                return resolution
        return resolution

    def profile(self, info):
        resolution = self.get_resolution(info)
        profile = '%sp.%s' % (resolution, self.format)
        return profile

    def cmd(self, args):
        filename = args[0]
        if len(filename) == 16:
            path = self.path(filename)
        else:
            path = [filename]
        for p in path:
            if os.path.exists(p):
                info = utils.avinfo(p)
                profile = self.profile(info)
                cmd = encode_cmd(p, self.media_cache(), profile, info)
                cmd = [' ' in c and u'"%s"' % c or c for c in cmd]
                print (u' '.join(cmd)).encode('utf-8')

    def save_config(self):
        if not self._configfile:
            raise Exception('Can not save temporary config')
        with open(self._configfile, 'w') as f:
            json.dump(self._config, f, indent=2)

    def config(self, args):
        print "Current Config:\n  User: %s\n  URL: %s\n" %(self._config['username'], self._config['url'])
        print "Leave empty to keep current value\n"
        username = raw_input('Username: ')
        if username:
            self._config['username'] = username
        password = getpass.getpass('Password: ')
        if password:
            self._config['password'] = password
        url = raw_input('Pan.do/ra URL(i.e. http://pad.ma/api/): ')
        if url:
            self._config['url'] = url
        self.save_config()
        print "\nconfiguration updated."
        self.install_programs()

    def install_programs(self, args=[]):
        update = 'update' in args
        #install required programs
        if sys.platform == 'darwin':
            osext = 'macosx'
        elif sys.platform == 'win32':
            osext = 'exe'
        else:
            osext = 'linux'
        bindir = os.path.expanduser('~/.ox/bin')
        ox.makedirs(bindir)
        for p in ('ffmpeg', 'ffmpeg2theora'):
            path = os.path.join(bindir, p)
            if sys.platform == 'win32':
                p += '.exe'
            if not os.path.exists(path) or update:
                print "installing %s in %s" % (p, bindir)
                ox.net.save_url('http://firefogg.org/bin/%s.%s' % (p, osext), path, True)
                os.chmod(path, 0755)

    def add_volume(self, args):
        usage = "Usage: %s add_volume name path" % sys.argv[0]
        if len(args) != 2:
            print usage
            sys.exit(1)
        name = args[0]
        path = os.path.abspath(args[1])
        if not path.endswith('/'):
            path += '/'
        if os.path.isdir(path):
            if name in self._config['volumes']:
                print "updated %s to %s" % (name, path)
            else:
                print "added %s %s" % (name, path)
            self._config['volumes'][name] = path
            self.save_config()
        else:
            print "'%s' does not exist"  % path
            print usage
            sys.exit(1)

    def active_volumes(self):
        volumes = {}
        for name in sorted(self._config['volumes']):
            path = self._config['volumes'][name]
            path = os.path.normpath(path)
            if not path.endswith('/'):
                path += '/'
            if isinstance(path, str):
                path = path.decode('utf-8')
            if os.path.exists(path):
                volumes[name] = path
        return volumes

    def scan(self, args):
        rescan = 'rescan' in args
        print "checking for new files ..."
        volumes = self.active_volumes()
        for name in sorted(volumes):
            path = volumes[name]
            conn, c = self._conn()
            c.execute(u'SELECT path FROM file WHERE path LIKE ? AND deleted < 0', [u"%s%%" % path])
            known_files = [r[0] for r in c.fetchall()]

            files = []
            unknown = []
            ignored = []
            unsupported = []
            for dirpath, dirnames, filenames in os.walk(path, followlinks=True):
                if filenames:
                    for filename in sorted(filenames):
                        file_path = os.path.join(dirpath, filename)
                        if not ignore_file(self, file_path):
                            files.append(file_path)
                        else:
                            ignored.append(file_path)
            for f in files:
                if not parse_path(self, f[len(path):]):
                    unknown.append(f)

            files = list(set(files) - set(unknown))

            for f in files:
                if not self.scan_file(f, rescan):
                    unsupported.append(f)

            if unknown:
                example = example_path(self)
                print 'Files need to be in a folder structure like this:\n%s\n' % example
                print 'The following files do not fit into the folder structure and will not be synced:'
                print '\t',
                print '\n\t'.join([f[len(path):].encode('utf-8') for f in unknown])
                print ''

            if unsupported:
                files = list(set(files) - set(unsupported))
                print 'The following files are in an unsupported format and will not be synced:'
                print '\t',
                print '\n\t'.join([f[len(path):] for f in unsupported])
                print ''
            '''
            '''

            deleted_files = filter(lambda f: f not in files, known_files)
            new_files = filter(lambda f: f not in known_files, files)
            conn, c = self._conn()
            if deleted_files:
                deleted = time.mktime(time.localtime())
                for f in deleted_files:
                    c.execute(u'UPDATE file SET deleted=? WHERE path=?', (deleted, f))
                conn.commit()

            '''
            print "scanned volume %s: %s files, %s new, %s deleted, %s ignored, %s unsupported" % (
                    name, len(files), len(new_files), len(deleted_files), len(ignored), len(unsupported))
            '''
            print "scanned volume %s: %s files, %s new, %s deleted, %s ignored" % (
                    name, len(files), len(new_files), len(deleted_files), len(ignored))


    def extract(self, args):
        conn, c = self._conn()
        if args:
            if args[0] == 'offline':
                files = self.get_encodes(self._config['url'])
            elif args[0] == 'all':
                files = []
                for name in self._config['volumes']:
                    path = self._config['volumes'][name]
                    path = os.path.normpath(path)
                    if not path.endswith('/'):
                        path += '/'
                    if os.path.exists(path):
                        files += self.files(path)['info']
            else:
                files = [f if len(f) == 16 else ox.oshash(f) for f in args]
        else:
            if not self.user:
                print "you need to login or run pandora_client extract offline"
                return
            self.update_encodes()
            files = self.get_encodes(self._config['url'])

        for oshash in files:
            info = self.info(oshash)
            if not 'error' in info:
                for path in self.path(oshash):
                    if os.path.exists(path):
                        profile = self.profile(info)
                        i = encode(path, self.media_cache(), profile, info,
                                self.importFrames)
                        break

    def sync(self, args):
        if not self.user:
            print "you need to login"
            return
        conn, c = self._conn()

        volumes = self.active_volumes()
        if not volumes:
            print "no active volumes found"
            return

        for name in sorted(volumes):
            prefix = volumes[name]
            files = self.files(prefix)
            post = {}
            post['files'] = files['files']
            post['volume'] = name
            print 'sending list of files in %s (%s total)' % (name, len(post['files']))
            r = self.api.update(post)
            if r['status']['code'] == 200:
                #backend works on update request asyncronously, wait for it to finish
                if 'taskId' in r['data']:
                    t = self.api.taskStatus(task_id=r['data']['taskId'])
                    print 'waiting for server ...'
                    while t['data']['status'] == 'PENDING':
                        time.sleep(5)
                        t = self.api.taskStatus(task_id=r['data']['taskId'])
                    #send empty list to get updated list of requested info/files/data
                    post = {'info': {}}
                    r = self.api.update(post)

                if r['data']['info']:
                    info = r['data']['info']
                    max_info = 100
                    total = len(info)
                    sent = 0
                    for offset in range(0, total, max_info):
                        post = {'info': {}, 'upload': True}
                        post['info'] = self.get_info_for_ids(info[offset:offset+max_info], prefix)
                        if len(post['info']):
                            r = self.api.update(post)
                            sent += len(post['info'])
                    if sent:
                        print 'sent info for %s files' % sent
                    #send empty list to get updated list of requested info/files/data
                    post = {'info': {}}
                    r = self.api.update(post)

        if not 'data' in r:
            print r
            return

        if r['data']['data']:
            files = []
            for f in r['data']['data']:
                for path in self.path(f):
                    if os.path.exists(path):
                        files.append(path)
                        break
            if files:
                print '\ncould encode and upload %s videos:\n' % len(files)
                print '\n'.join(files)
        if r['data']['file']:
            files = []
            for f in r['data']['file']:
                for path in self.path(f):
                    if os.path.exists(path):
                        files.append(path)
                        break
            if files:
                print '\ncould upload %s subtitles:\n' % len(files)
                print '\n'.join(files)

    def upload(self, args):
        if not self.user:
            print "you need to login"
            return
        conn, c = self._conn()
        if args:
            data = []
            for arg in args:
                if os.path.exists(arg):
                    oshash = ox.oshash(arg)
                    self.scan_file(arg)
                    r = self.api.findMedia({'query': {
                        'conditions': [{'key': 'oshash', 'value': oshash}]
                    }})['data']['items']
                    if r == 0:
                        info = self.info(oshash)
                        filename = os.path.basename(arg)
                        r = self.api.addMedia({
                            'id': oshash,
                            'info': info,
                            'filename': filename
                        })
                    data.append(oshash)
                else:
                    data.append(arg)
            files = []
            info = []
        else:
            #send empty list to get updated list of requested info/files/data
            post = {'info': {}}
            r = self.api.update(post)
            data = r['data']['data']
            files = r['data']['file']
            info = r['data']['info']
        
        if info:
            print 'info for %d files requested' % len(info)
            max_info = 100
            total = len(info)
            sent = 0
            for offset in range(0, total, max_info):
                post = {'info': {}, 'upload': True}
                post['info'] = self.get_info_for_ids(info[offset:offset+max_info])
                if len(post['info']):
                    r = self.api.update(post)
                    sent += len(post['info'])
            if sent:
                print 'uploading info for %d files' % sent

        if data:
            print 'encoding and uploading %s videos' % len(data)
            for oshash in data:
                data = {}
                info = self.info(oshash)
                if info and not 'error' in info:
                    for path in self.path(oshash):
                        if os.path.exists(path):
                            if not self.api.uploadVideo(path,
                                                    data, self.profile(info), info):
                                print 'video upload failed, giving up, please try again'
                                return
                            if 'rightsLevel' in self._config:
                                r = self.api.find({'query': {
                                    'conditions': [
                                        {'key': 'oshash', 'value': oshash, 'operator': '=='}
                                    ],
                                    'keys': ['id'],
                                    'range': [0, 1]
                                }})
                                if r['data']['items']:
                                    item = r['data']['items'][0]['id']
                                    r = self.api.edit({
                                        'item': item,
                                        'rightsLevel': self._config['rightsLevel']
                                    })
                            break

        if files:
            print 'uploading %s files' % len(files)
            for oshash in files:
                for path in self.path(oshash):
                    if os.path.exists(path):
                        self.api.uploadData(path, oshash)
                        break

    def upload_frames(self, args):
        if not self.user:
            print "you need to login"
            return
        conn, c = self._conn()
        for oshash in args:
            info = self.info(oshash)
            if info and not 'error' in info:
                for path in self.path(oshash):
                    if os.path.exists(path):
                        frames = get_frames(path, self.api.media_cache, info, True)
                        i = {
                            'info': info,
                            'oshash': oshash,
                            'frames': frames,
                        }
                        r = self.api.uploadFrames(i, {})
                        if r.get('status', {}).get('code') != 200:
                            print r

    def upload_document(self, args):
        if not self.user:
            print "you need to login"
            return
        conn, c = self._conn()
        for f in args:
            if f.split('.')[-1] not in ('jpg', 'pdf', 'png'):
                print 'unsupported format', f
                continue
            url = '%supload/document/' % self._config['url']
            r = self.api.upload_chunks(url, f, {
                'filename': os.path.basename(f)
            })
            '''
            if r:
                oshash = ox.oshash(f)
                r = self.api.findDocuments({
                    "keys": ['id'],
                    "query": {
                        "conditions": [{"key": 'oshash', "value": oshash, "operator": '=='}],
                        "operator": '&'
                    }
                })
                did = r['data']['items'][0]['id']
                if description:
                    r = api.editDocument({
                        'id': did,
                        'description': descriptoin
                    })
                if item:
                    r = api.addDocument({
                        'id': did,
                        'item': item
                    })
            '''

    def files(self, prefix):
        if not prefix.endswith('/'):
            prefix += '/'
        conn, c = self._conn()
        files = {}
        files['info'] = {}
        files['files'] = []
        sql = u'SELECT path, oshash, info, atime, ctime, mtime FROM file WHERE deleted < 0 AND path LIKE ? ORDER BY path'
        t = [u"%s%%"%prefix]
        c.execute(sql, t)
        for row in c:
            path = row[0]
            oshash = row[1]
            info = json.loads(row[2])
            if not 'error'  in info:
                for key in ('atime', 'ctime', 'mtime', 'path'):
                    if key in info:
                        del info[key]
                files['info'][oshash] = info
                files['files'].append({
                    'oshash': oshash,
                    'path': path[len(prefix):],
                    'atime': row[3],
                    'ctime': row[4],
                    'mtime': row[5],
                })
        return files

    def clean(self, args):
        if os.path.exists(self.api.media_cache):
            if args and args[0] == 'all':
                print "remove all cached videos in", self.api.media_cache

                #if os.path.exists(self.api.media_cache):
                #    shutil.rmtree(self.api.media_cache)
            else:
                nothing = False
                for root, folders, files in os.walk(self.api.media_cache):
                    for f in files:
                        f = os.path.join(root, f)
                        if f.endswith('.webm'):
                            oshash = os.path.dirname(f)[len(self.api.media_cache):].replace('/', '')
                            remove = True
                            for path in self.path(oshash):
                                if os.path.exists(path):
                                    remove = False
                                    break
                            if remove:
                                nothing = False
                                os.unlink(f)
                if nothing and folders:
                    print "No unused files found in cache, run \"%s clean all\" to remove the entire cache" % sys.argv[0]
                else:
                    utils.cleanup_tree(self.api.media_cache)

    def import_srt(self, args):
        '''
            import srt as annotations, usage:
                pandora_client ITEMID layername /path/to/transcript.srt
            i.e. 
                pandora_client ABC transcripts /path/to/transcript.srt
        '''
        if not args:
            print 'Usage: pandora_client ABC transcripts /path/to/transcript.srt'
            sys.exit(1)
        item = args[0]
        layer = args[1]
        filename = args[2]
        layers = [l['id'] for l in self.api.site['layers']]
        if layer not in layers:
            print "invalid layer name, choices are: ", ', '.join(layers)
            sys.exit(1)
        annotations = [{
            'in': s['in'],
            'out': s['out'],
            'value': s['value'].replace('\n', '<br>\n') if layer == 'subtitles' else s['value'],
        } for s in ox.srt.load(filename)]
        r = self.api.addAnnotations({
            'item': item,
            'layer': layer,
            'annotations': annotations
        })
        if r['status']['code'] == 400:
            print 'failed'
            sys.exit(1)
        if r['status']['code'] == 403:
            print 'permission deinied'
            sys.exit(1)
        elif r['status']['code'] == 404:
            print 'item not found'
            sys.exit(1)

    def server(self, args):
        import server
        server.run(self)

    def client(self, args):
        if not args:
            print 'usage: %s client <server_url>\n\ti.e. %s client http://192.168.1.1:8789' % (sys.argv[0], sys.argv[0])
            sys.exit(1)
        import client
        url = args[0]
        if len(args) == 1:
            name = socket.gethostname()
        else:
            name = args[1]
        c = client.DistributedClient(url, name)
        c.run()

class API(ox.API):
    __name__ = 'pandora_client'
    __version__ = __version__

    def __init__(self, url, cj=None, media_cache=None):
        super(API, self).__init__(url, cj)

        self.media_cache = media_cache
        if not self.media_cache:
            self.media_cache = os.path.expanduser(default_media_cache)
        netloc = urlparse(self.url).netloc
        self._resume_file = '/tmp/pandora_client.%s.%s.json' % (os.environ.get('USER'), netloc)

    def uploadFrames(self, i, data):
        #upload frames
        if self.site['media'].get('importFrames') and i['frames']:
            form = ox.MultiPartForm()
            form.add_field('action', 'upload')
            form.add_field('id', i['oshash'])
            for key in data:
                form.add_field(key, data[key])
            for frame in i['frames']:
                fname = os.path.basename(frame)
                if os.path.exists(frame):
                    form.add_file('frame', fname, open(frame, 'rb'))
            r = self._json_request(self.url, form)
            return r

    def uploadVideo(self, filename, data, profile, info=None):
        i = encode(filename, self.media_cache, profile, info,
                   self.site['media'].get('importFrames'))
        if not i:
            print "failed"
            return

        #upload frames
        r = self.uploadFrames(i, data)

        #upload media 
        if os.path.exists(i['media']):
            size = ox.format_bytes(os.path.getsize(i['media']))
            name = os.path.basename(filename)
            print (u"uploading %s of %s (%s)" % (profile, name, size)).encode('utf-8')
            url = self.url + 'upload/?profile=%s&id=%s' % (profile, i['oshash'])
            if not self.upload_chunks(url, i['media'], data):
                if DEBUG:
                    print "failed"
                return False
        else:
            print "Failed"
            return False
        return True

    def uploadData(self, filename, oshash):
        if DEBUG:
            print 'upload', filename
        form = ox.MultiPartForm()
        form.add_field('action', 'upload')
        form.add_field('id', str(oshash))
        fname = os.path.basename(filename)
        if isinstance(fname, unicode): fname = fname.encode('utf-8')
        form.add_file('file', fname, open(filename, 'rb'))
        r = self._json_request(self.url, form)
        return r

    def upload_chunks(self, url, filename, data=None):
        form = ox.MultiPartForm()
        resume = None
        if os.path.exists(self._resume_file):
            with open(self._resume_file) as f:
                try:
                    resume = json.load(f)
                except:
                    resume = {}
            if resume.get('chunkUploadUrl') != url:
                resume = None
        if resume:
            data = resume
        else:
            for key in data:
                form.add_field(key, data[key])
            data = self._json_request(url, form)

        print filename
        hide_cursor()
        result_url = data.get('url')
        if 'uploadUrl' in data:
            uploadUrl = data['uploadUrl']
            if uploadUrl.startswith('/'):
                u = urlparse(url)
                uploadUrl = '%s://%s%s' % (u.scheme, u.netloc, uploadUrl)
            f = open(filename)
            fsize = os.stat(filename).st_size
            done = 0
            start = time.mktime(time.localtime())
            if 'offset' in data and data['offset'] < fsize:
                done = data['offset']
                f.seek(done)
                resume_offset = done
            else:
                resume_offset = 0
            chunk = f.read(CHUNK_SIZE)
            fname = os.path.basename(filename)
            if isinstance(fname, unicode):
                fname = fname.encode('utf-8')
            while chunk:
                elapsed = time.mktime(time.localtime()) - start
                remaining = ""
                if done:
                    r = math.ceil((elapsed / (done/(fsize-resume_offset)) - elapsed)/60) * 60 * 1000 
                    r = ox.format_duration(r, milliseconds=False, verbosity=2)
                    if r:
                        remaining = ", %s remaining" % r
                msg = '%0.2f%% %s of %s done%s' % (
                    100 * done/fsize, ox.format_bytes(done), ox.format_bytes(fsize), remaining)
                print ''.join([msg, ' ' * (80-len(msg)), '\r']),
                sys.stdout.flush()
                form = ox.MultiPartForm()
                form.add_file('chunk', fname, chunk)
                if len(chunk) < CHUNK_SIZE or f.tell() == fsize:
                    form.add_field('done', '1')
                form.add_field('offset', str(done))
                try:
                    data = self._json_request(uploadUrl, form)
                except KeyboardInterrupt:
                    print "\ninterrupted by user."
                    sys.exit(1)
                except:
                    print "uploading chunk failed, will try again in 5 seconds\r",
                    sys.stdout.flush()
                    if DEBUG:
                        print '\n', uploadUrl
                        import traceback
                        traceback.print_exc()
                    data = {'result': -1}
                    time.sleep(5)
                if data and 'status' in data:
                    if data['status']['code'] == 403:
                        print "login required"
                        return False
                    if data['status']['code'] != 200:
                        print "request returned error, will try again in 5 seconds"
                        if DEBUG:
                            print data
                        time.sleep(5)
                if data and data.get('result') == 1:
                    done += len(chunk)
                    if data.get('offset') not in (None, done):
                        print 'server offset out of sync, continue from', data['offset']
                        done = data['offset']
                        f.seek(done)
                    with open(self._resume_file, 'w') as r:
                        json.dump({
                            'uploadUrl': uploadUrl,
                            'chunkUploadUrl': url,
                            'url': result_url,
                            'offset': done
                        }, r, indent=2)
                    chunk = f.read(CHUNK_SIZE)
            if os.path.exists(self._resume_file):
                os.unlink(self._resume_file)
                resume = None
            if result_url:
                print result_url + (' ' * (80-len(result_url)))
            else:
                print ' ' * 80
            print ''
            show_cursor()
            return data and 'result' in data and data.get('result') == 1
        else:
            if DEBUG:
                if 'status' in data and data['status']['code'] == 401:
                    print "login required"
                else:
                    print "failed to upload file to", url
                    print data
        return False

