#!/usr/bin/env python
import os
import sys
import json
import netrc
import argparse
import subprocess

from cdl.signin import get_cookie, format_cookie
from cdl.parser import parse, generate_download_script

LECTURE_URL = 'https://class.coursera.org/%s/lecture'


def from_netrc():
    filename = os.path.expanduser('~/.netrc')
    if os.path.exists(filename):
        rc = netrc.netrc(filename)
        for key in ('accounts.coursera.org', 'coursera.org'):
            if key in rc.hosts:
                login, _, password = rc.hosts[key]
                return login, password
    return None, None


def main():
    args = parse_args()
    os.chdir(args.output_dir)

    if not os.path.exists('cookie'):
        cookie = get_cookie(args.user, args.password, args.proxy)
        cookie_string = format_cookie(cookie)
        with open('cookie', 'w') as file:
            file.write(cookie_string)
        with open('cookie.json', 'w') as file:
            json.dump(cookie, file)

    url = LECTURE_URL % args.course_id
    with open('url', 'w') as file:
        file.write(url)

    cmd = 'wget --no-cookies --header "Cookie: $(cat cookie)" -O index \'%s\' ' % url
    subprocess.call(cmd, shell=True)

    with open('index') as file:
        result = parse(file.read())

    toc = []
    for chapter, content in result:
        toc.append(chapter.encode('utf8'))
        for lecture, links in content:
            toc.append('- ' + lecture.encode('utf8'))
        toc.append('')
    toc = os.linesep.join(toc)
    with open('toc', 'w') as file:
        file.write(toc)

    codes = generate_download_script(result)
    with open('download.sh', 'w') as file:
        file.write(os.linesep.join(codes))

    if not args.dry_run:
        subprocess.call(['bash', '-x', 'download.sh'])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('--proxy')
    parser.add_argument('-O', '--output-dir')
    parser.add_argument('-D', '--dry-run', action='store_true')
    parser.add_argument('course_id')
    args = parser.parse_args()

    if not args.user or not args.password:
        args.user, args.password = from_netrc()
    if not args.user or not args.password:
        print >> sys.stderr, """Can't find credentials, see -u and -p.

Or you can add line like this into your ~/.netrc file:
    machine acounts.coursera.org login <email> password <pass>"""
        sys.exit(1)

    if not args.output_dir:
        args.output_dir = args.course_id
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    elif not os.path.isdir(args.output_dir):
        print >> sys.stderr, "Not a directory:", args.output_dir
        sys.exit(1)

    if not args.proxy and 'http_proxy' in os.environ:
        args.proxy = os.environ['http_proxy']

    return args


if __name__ == '__main__':
    main()
