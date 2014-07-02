#!/usr/local/opt/python/bin/python2.7
'''
Based on Andrew Jennings' [gmail-backup](https://github.com/abjennings/gmail-backup)
'''

import calendar
import ConfigParser
import email
import email.utils
import fcntl
import getpass
import gnupg
import hashlib
import imaplib
import os
import re
import StringIO
import sys
import tarfile

UID_RE = re.compile(r'\d+\s+\(UID (\d+)\)$')

def get_uid(server, n):
    resp, lst = server.fetch(n, 'UID')
    m = UID_RE.match(lst[0])
    if not m:
        raise Exception('Internal error parsing UID response: %s %s.  Please try again' \
            % (resp, lst))
    return m.group(1)

def extract_timestamp(message):
    msg = email.message_from_string(message)
    date = email.utils.parsedate_tz(msg['Date'])

    timestamp = 0
    
    if date is None:
        pass
    elif date[9] is None:
        # If there was no timezone found, don't adjust the time.
        timestamp = calendar.timegm(date)
    else:
        # We have a valid date, adjust it to UTC.        
        timestamp = calendar.timegm(date) - date[9]

    return timestamp

def download_message(server, n, gpg, config):
    resp, lst = server.fetch(n, '(RFC822)')
    if resp != 'OK':
        raise Exception('Bad response: %s %s' % (resp, lst))

    plaintext = lst[0][1]
    timestamp = extract_timestamp(plaintext)
    encrypted = gpg.encrypt(plaintext, config.get('gpg', 'keyid'), armor=False)

    return [encrypted.data, timestamp]

def open_meta_file(fname):
    meta = None

    if not os.path.isfile(fname):
        print 'Creating meta file ' + fname
        meta = open(fname, 'w+')
        meta.write('0')
        meta.seek(0)

    else:
        meta = open(fname, 'r+')

    return meta

def get_last_downloaded(meta_file):
    location = int(meta_file.read())
    meta_file.seek(0)
    return location

def update_meta_file(meta_file, last_downloaded, flush=True):
    meta_file.truncate()
    meta_file.write(str(last_downloaded))
    
    if flush:
        meta_file.flush()

    meta_file.seek(0)

def open_tar_file(fname):
    tar = None

    if not os.path.isfile(fname):
        print 'Creating tar file ' + fname
        tar = tarfile.open(name=fname, mode='w:')

    else:
        tar = tarfile.open(name=fname, mode='a:')

    return tar

def find_next_email(server, folder, last_downloaded):
    resp, [countstr] = server.select(folder, True)
    count = int(countstr)

    gotten, ungotten = 0, count + 1
    while (ungotten - gotten) > 1:
        attempt = (gotten + ungotten) / 2
        uid = get_uid(server, attempt)
        if int(uid) <= last_downloaded:
            print 'Finding starting point: %d/%d (UID: %s) too low' % (attempt, count, uid)
            gotten = attempt
        else:
            print 'Finding starting point: %d/%d (UID: %s) too high' % (attempt, count, uid)
            ungotten = attempt

    return (ungotten, count)

def archive_message(tar, encrypted, timestamp, uid):
    encrypted_f = StringIO.StringIO()
    encrypted_f.write(encrypted)
    encrypted_f.seek(0)

    info = tarfile.TarInfo(name = uid + '.eml.gpg')
    info.size = len(encrypted_f.buf)
    info.mtime = timestamp
    tar.addfile(tarinfo = info, fileobj = encrypted_f)

def do_backup(config):
    if config.getboolean('backup', 'onexternal') and \
        not os.path.exists(config.getboolean('backup', 'path')):

        print 'External drive not mounted. Terminating'
        exit(0)

    meta_file = open_meta_file(config.get('backup', 'path') + config.get('backup', 'metafile'))
    last_downloaded = get_last_downloaded(meta_file)
    print "Last email downloaded was %d" % last_downloaded

    tar = open_tar_file(config.get('backup', 'path') + config.get('backup', 'archive'))

    gpg = gnupg.GPG(config.get('gpg', 'binary'),
                    homedir = os.path.expanduser(config.get('gpg', 'home')))
    gpg.encoding = config.get('gpg', 'encoding')

    print 'Logging in as ' + config.get('gmail', 'username')
    server = imaplib.IMAP4_SSL(config.get('gmail', 'server'))
    server.login(config.get('gmail', 'username'), config.get('gmail', 'password'))

    # Find the email UID to start downloading.
    start, count = find_next_email(server, config.get('gmail', 'folder'), last_downloaded)

    try:
        for i in xrange(start, count + 1):
            uid = get_uid(server, i)
            print 'Downloading %d/%d (UID: %s)' % (i, count, uid)
            encrypted, timestamp = download_message(server, i, gpg, config)
            archive_message(tar, encrypted, timestamp, uid)

            last_downloaded = int(uid)

    finally:
        print 'Cleaning up. Last email downloaded was %d.' % last_downloaded
        update_meta_file(meta_file, last_downloaded)
        meta_file.close()
        tar.close()

        server.close()
        server.logout()

def read_config():
    config = ConfigParser.RawConfigParser()
    default_fname = os.path.dirname(os.path.abspath(__file__)) + '/defaults.ini'
    config.readfp(open(default_fname))
    
    user_fname = os.path.expanduser(config.get('config', 'filename'))
    config.read(['settings.ini', user_fname])

    # Last step is to check if the user explicitly passed in a config file.
    if len(sys.argv) > 1:
        arg_fname = os.path.expanduser(sys.args[1])
        print 'Using ' + arg_fname
        config.read(arg_fname)

    return config

def singleton_lock(config):
    pid_file = None

    if config.getboolean('backup', 'use_pid'):
        # Use the hash of the username for the PID.
        # This allows backup of multiple users at the same time.
        username_hash = hashlib.md5(config.get('gmail', 'username')).hexdigest()
        pid_fname = '%s.%s.pid' % (config.get('backup', 'pid_prefix'), username_hash)

        pid_file = open(pid_fname, 'w')
        try:
            fcntl.lockf(pid_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            print 'Another instance is running for %s, terminating.' \
                % config.get('gmail', 'username')

            sys.exit(0)

    return pid_file

def main():
    config = read_config()

    # Ensure only one copy of the script is running per username.
    pid_file = singleton_lock(config)

    try:
        do_backup(config)
    except KeyboardInterrupt:
        print 'Stopping.'

if __name__ == '__main__':
    main()
