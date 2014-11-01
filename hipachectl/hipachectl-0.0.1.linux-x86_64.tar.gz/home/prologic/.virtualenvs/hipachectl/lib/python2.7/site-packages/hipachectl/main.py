#!/usr/bin/env python
# Module:   main
# Date:     1st November 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Command Line Tool to Manage hipache"""


from __future__ import print_function

from os import environ
from argparse import ArgumentParser


from redis import StrictRedis
from urlparse import urlparse


def add_virtualhost(r, args):
    url = format_url(args.ip, args.port)
    vhost = "frontend:{0:s}".format(args.vhost)
    if vhost in r.keys():
        members = r.lrange(vhost, 0, -1)
        if args.id in members:
            if url not in members:
                r.linsert(vhost, "after", args.id, url)
        else:
            r.rpush(vhost, args.id)
            r.rpush(vhost, url)
    else:
        r.rpush(vhost, args.id)
        r.rpush(vhost, url)


def delete_virtualhost(r, args):
    vhost = "frontend:{0:s}".format(args.vhost)
    if not args.ip:
        r.delete(vhost, args.id)
    else:
        url = format_url(args.ip, args.port)
        r.lrem(vhost, 0, url)


def format_url(ip, port):
    port = "" if port in (80, 443) else ":{0:d}".format(port)
    scheme = "https" if port == 443 else "http"
    url = "{0:s}://{1:s}{2:s}".format(scheme, ip, port)
    return url


def list_virtualhosts(r, args):
    for i, k in enumerate(r.keys()):
        vhost = k.split(":")[1]
        id, url = r.lrange(k, 0, -1)
        print("{0:d}. {1:s} {2:s} {3:s}".format(i, vhost, id, url))


def parse_args():
    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
        "-H", dest="host", metavar="HOST", type=str,
        help="hipache Redis Host", default="127.0.0.1"
    )

    parser.add_argument(
        "-P", dest="rport", metavar="RPORT", type=int,
        help="hipache Redis Port", default=6379
    )

    parser.add_argument(
        "-D", dest="database", metavar="DATABASE", type=int,
        help="hipache Redis Database", default=0
    )

    parser.add_argument(
        "-A", dest="password", metavar="PASSWORD", type=str,
        help="hipache Redis Database Password", default=None
    )

    parser.add_argument(
        "-U", dest="url", metavar="URL", type=str,
        help="hipache Redis Connection URL (optional)", default=None
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        description="Available Commands",
        help="Description"
    )

    # add
    add_parser = subparsers.add_parser(
        "add",
        help="Add VirtualHost"
    )
    add_parser.set_defaults(func=add_virtualhost)

    add_parser.add_argument(
        "-i", "--ip", dest="ip", default=None, metavar="IP", type=str,
        help="IP Address"
    )

    add_parser.add_argument(
        "-p", "--port", dest="port", default=80, metavar="PORT", type=int,
        help="HTTP Listening Port"
    )

    add_parser.add_argument(
        "id", metavar="ID", type=str,
        help="Container Name or CID"
    )

    add_parser.add_argument(
        "vhost", metavar="VHOST", type=str,
        help="Application VirtualHost"
    )

    # delete
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete VirtualHost"
    )
    delete_parser.set_defaults(func=delete_virtualhost)

    delete_parser.add_argument(
        "id", metavar="ID", type=str,
        help="Container Name or CID"
    )

    delete_parser.add_argument(
        "vhost", metavar="VHOST", type=str,
        help="Application VirtualHost"
    )

    delete_parser.add_argument(
        "-i", "--ip", dest="ip", default=None, metavar="IP", type=str,
        help="IP Address"
    )

    delete_parser.add_argument(
        "-p", "--port", dest="port", default=80, metavar="PORT", type=int,
        help="HTTP Listening Port"
    )

    # list
    list_parser = subparsers.add_parser(
        "list",
        help="List VirtualHosts"
    )
    list_parser.set_defaults(func=list_virtualhosts)

    return parser.parse_args()


def main():
    args = parse_args()

    if "REDIS_PORT" in environ:
        parsed = urlparse(environ["REDIS_PORT"])
        netloc = parsed.netloc
        host, port = netloc.split(":")
        args.host = host
        args.rport = port

    if args.url:
        parsed = urlparse(args.url)
        netloc = parsed.netloc
        creds, host = netloc.split("@")
        _, password = creds.split(":")
        host, port = host.split(":")
        args.host = host
        if port:
            args.rport = port
        if password:
            args.password = password
        if parsed.path:
            database = parsed.path.replace("/", "")
            args.database = int(database)

    r = StrictRedis(host=args.host, port=args.rport, db=args.database,
                    password=args.password)
    args.func(r, args)


if __name__ == "__main__":
    main()
