#!/usr/bin/env python

import os
import time
import re

import requests
import tpb

#curl -X POST -d '{"method":"torrent-add","arguments":{"paused":false,"download-dir":"xxx","filename":"xxx"}}' http://127.0.0.1:9090/transmission/rpc --header 'X-Transmission-Session-Id:asddkdfjidfijdaf'

sesh_url = '%s/transmission/web'
rpc_url = '%s/transmission/rpc'

re_size = re.compile(r'(\d*\.?\d*)\s*(\w*)')

def create_session(host):
    res = requests.get(sesh_url % host)
    return {
        'x-transmission-session-id': res.headers['x-transmission-session-id']
    }

def add_magnet_url(host, download_dir, url, hdr):
    res = requests.post(rpc_url % host, headers=hdr,
            data='{"method":"torrent-add","arguments":{"paused":false,"download-dir":"%s","filename":"%s"}}' % (download_dir, url))
    assert res.status_code == 200, 'Status Code fail: %s, %d' % (
        url, res.status_code)
    return res

def convert_size(size_str):
    amt, order = re_size.match(size_str).groups()
    amt = float(amt)
    order = order.lower()
    if order in ('kb', 'k', 'kib'):                                                      
        size = amt * 2**10                                                  
    elif order in ('mb', 'm', 'mib'):                                                    
        size = amt * 2**20                                                  
    elif order in ('gb', 'g', 'gib'):                                                    
        size = amt * 2**30                                                  
    elif order in ('tb', 't', 'tib'):                                                    
        size = amt * 2**40                                                  
    elif order in ('pb', 'p', 'pib'):                                                    
        size = amt * 2**50                                                  
    elif order in ('', 'b'):
        size = int(amt)
    else:                                                                   
        raise RuntimeError('Unknown size order: %s' % order)     
    return size

def search_pirate_bay(search_str, min_size=100 * 2**20, min_seeders=10,
    max_size=10 * 2**30, max_torrents=10):
    bay = tpb.TPB('https://thepiratebay.org')

    num = 0
    ret = []
    search = bay.search(search_str)
    for torrent in search.order(tpb.ORDERS.SEEDERS.DES).multipage():
        if num >= max_torrents:
            break
        num += 1
        if torrent.seeders < min_seeders:
            # Ordered by seeders, so at this point there aren't enough anymore
            break
        size = convert_size(torrent.size)
        if size < min_size or size > max_size:
            continue
        info = torrent.info
        magnet = torrent.magnet_link
        ret += [torrent]
    return ret

def output_torrent(i):
    print('%-10s: %s' % ('title', i.title))
    print('%-10s: %s' % ('size', i.size))
    print('%-10s: %s' % ('info', '\n'.join(i.info.splitlines()[:5])))
    
def download_loop(args):
    downloading = []
    while True:
        print('searching...')
        search = search_pirate_bay(args.search_string,
            min_size=convert_size(args.min_size),
            max_size=convert_size(args.max_size),
            min_seeders=args.seeders,
            max_torrents=args.max_search)
        hdr = create_session(args.host)
        for i in search:
            if i.magnet_link in downloading:
                continue
            if args.verbose:
                output_torrent(i)
            print('%s' % i.magnet_link)
            res = add_magnet_url(args.host, args.download_dir, i.magnet_link, hdr)  
            downloading += [i.magnet_link]
            if args.verbose:
                print('response status: %d' % res.status_code)
            if len(downloading) >= args.max_download:
                break
        if len(downloading) >= args.max_download:
            break
        if args.interval is None:
            break
        else:
            time.sleep(args.interval)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--min-size', '-m', default="100MB",
        help='minimum size of files (eg. 1GB,2MB,5.2T,100)')
    parser.add_argument('--max-size', '-M', default="10GB",
        help='maximum size of files (eg. 1GB,2MB,5.2T,100)')
    parser.add_argument('--seeders', '-s', type=int, default=10,
        help='minimum number of seeders')
    parser.add_argument('--max-search', '-S', type=int, default=25,
        help='max torrents to check when searching')
    parser.add_argument('--verbose', '-v', action='store_true',
        help='verbose output')
    parser.add_argument('--interval', '-i', metavar='SECONDS', type=int,
        default=None,
        help='Keep running every SECONDS seconds without adding duplicates.\n'
            'Default behavior is to run once.')
    parser.add_argument('--max-download', '-d', type=int, default=10,
        help='max torrents to have downloading (quits continuous interval)')
    parser.add_argument('--host', '-H', 
        default='http://127.0.0.1:9090',
        help='transmission web host (default http://127.0.0.1:9090')
    parser.add_argument('--download-dir', '-D',
        default=os.path.join(os.getenv('HOME'), 'Downloads'),
        help='directory to download torrents to on transmission server')
    parser.add_argument('search_string')
    args = parser.parse_args()
    print 'Downloading to %s' % args.download_dir

    download_loop(args)

if __name__ == '__main__':
    main()
