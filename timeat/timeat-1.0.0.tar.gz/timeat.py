#!/usr/bin/env python
# Using Google maps API to get the current time at a given location

from socket import AF_INET, SOCK_DGRAM, socket, error as SocketError
from time import time, gmtime, strftime
from datetime import datetime
import json
import struct
import sys

__version__ = '1.0.0'

if sys.version_info[:2] >= (3, 0):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib import urlopen, urlencode

api_base = 'https://maps.googleapis.com/maps/api'
geo_url = '{}/geocode/json'.format(api_base)
tz_url = '{}/timezone/json'.format(api_base)


def get_json(url):
    fo = urlopen(url)
    data = fo.read().decode('utf-8')
    return json.loads(data)


def current_time():
    '''Try to get current time from NTP server, default to local if can't get
    it.'''
    sock = socket(AF_INET, SOCK_DGRAM)
    msg = ('\x1b' + 47 * '\0').encode('ascii')
    try:
        sock.settimeout(2)
        sock.sendto(msg, ('pool.ntp.org', 123))
    except SocketError:
        return int(time())

    msg, _ = sock.recvfrom(1024)

    t = struct.unpack("!12I", msg)[10]
    return t - 2208988800  # 1970-01-01 00:00:00


def timeat(location):
    '''Get local time at location, returns an interable of (place, time)'''
    query = urlencode([('address', location)])
    url = '{}?{}'.format(geo_url, query)
    loc_resp = get_json(url)
    if loc_resp['status'] != 'OK':
        return

    now = current_time()
    for loc in loc_resp['results']:
        geo = loc['geometry']['location']
        query = urlencode([
            ('timestamp', str(now)),
            ('location', '{},{}'.format(geo['lat'], geo['lng'])),
        ])
        url = '{}?{}'.format(tz_url, query)
        tz = get_json(url)

        timestamp = now + tz['dstOffset'] + tz['rawOffset']
        local = datetime.utcfromtimestamp(timestamp)
        yield loc['formatted_address'], local


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser()
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument('location', help='location to get time at')
    args = parser.parse_args(argv[1:])

    try:
        n = 0
        for n, (addr, local) in enumerate(timeat(args.location), 1):
            timestamp = local.strftime('%a %b %d, %Y %H:%M')
            print('{}: {}'.format(addr, timestamp))

        if n == 0:
            raise SystemExit(
                'error: cannot find time for `{}`'.format(args.location))

    except IOError as e:
        raise SystemExit('error: {}'.format(e))

if __name__ == '__main__':
    main()
