#!/usr/bin/env python
import socket
import re
from subprocess import check_output
from collections import namedtuple

import db

NMAP_CLI = 'nmap -p %(port)s -P0 -A -n %(host)s'
RE_IP = re.compile(
    r'Nmap scan report for '
    r'(?P<host>\S+) \((?P<ip>\d+\.\d+\.\d+\.\d+)\)'
)
RE_STATUS = re.compile(
    r'(?P<port>\d+)/\S+\s+(?P<state>\S+)\s+\S+\s+(?P<version>.*)$')

RE_KEY = re.compile(
    r'\|(?:\s+|_)(?:ssh-hostkey:\s+)?(?P<size>\d+)\s+(?P<fingerprint>(?:\w\w\:)+\w\w)'
    r'\s+\((?P<type>\w+)\)')

def grab_banner(host, port):
    sock = socket.socket()
    sock.connect((host, port))
    try:
        banner = sock.recv(4096)
    finally:
        sock.close()
    return banner

def scan_host(host, port):
    args = (NMAP_CLI % {'port': port, 'host': host}).split()
    out = check_output(args).splitlines()
    data = {}
    data['keys'] = []
    data['host'] = host
    data['ip'] = host
    for line in out:
        match_ip = RE_IP.match(line)
        if match_ip:
            data['host'] = match_ip.group('host')
            data['ip'] = match_ip.group('ip')
            continue
        match_status = RE_STATUS.match(line)
        if match_status:
            data['port'] = match_status.group('port')
            data['state'] = match_status.group('state')
            data['version'] = match_status.group('version')
            continue
        match_key = RE_KEY.match(line)
        if match_key:
            data['keys'] += [{
                'type': match_key.group('type'),
                'size': int(match_key.group('size')),
                'fingerprint': match_key.group('fingerprint'),
            }]
            continue
    if data.get('state') == 'open':
        data['banner'] = grab_banner(host, port)
    else:
        data['state'] = 'filtered'
        data['banner'] = ''
    return data

def query(hostname, username, password):
    session = db.connect(username, password)
    hosts = session.query(db.Host).filter_by(hostname=hostname).all()
    for host in hosts:
        print('%-16s: %s' % ('Hostname', host.hostname))
        print('%-16s: %s:%s' % ('Address', host.ip, host.port))
        print('%-16s: %s' % ('State', host.state))
        print('%-16s: %s' % ('Version', host.version))
        print('%-16s: %s' % ('Banner', host.banner))
        for key in host.keys:
            print('\t%s: %s' % (key, key.fingerprint))
        # blank line
        print('')

def save_data(data, username, password):
    session = db.connect(username, password)
    if data['state'] == 'filtered':
        host = db.Host(
            hostname=data['host'],
            ip=data['ip'],
            state=data['state'],
        )
    else:
        host = db.Host(
            hostname=data['host'],
            ip=data['ip'],
            port=data['port'],
            state=data['state'],
            version=data['version'],
            banner=data['banner'],
        )
        for key in data['keys']:
            dbkey = db.Key(
                typ=key['type'],
                size=key['size'],
                fingerprint=key['fingerprint'],
            )
            host.keys += [dbkey]
    session.add(host)
    session.commit()

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=22)
    parser.add_argument('--db-user', nargs='?', 
        help='postgres username (default sshscanner)',
        default='sshscanner')
    parser.add_argument('--db-pass', nargs='?',
        help='postgres password (default ssh)',
        default='ssh')
    parser.add_argument('--skip-db', '-s', action='store_true',
        help='skip saving to postgresql database')
    parser.add_argument('--query', '-q', action='store_true',
        help='query database for hostname')
    parser.add_argument('host', help='IP or hostname to scan')
    args = parser.parse_args()
    if args.query:
        query(args.host, args.db_user, args.db_pass)
    else:
        from pprint import pprint
        data = scan_host(args.host, args.port)
        pprint(data)
        if not args.skip_db:
            save_data(data, args.db_user, args.db_pass)

if __name__ == '__main__':
    main()
    

