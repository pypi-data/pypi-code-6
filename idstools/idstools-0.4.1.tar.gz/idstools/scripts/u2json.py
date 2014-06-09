#! /usr/bin/env python
#
# Copyright (c) 2014 Jason Ish
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Read unified2 log files and output events as JSON.

::

    usage: u2json [-h] [-C <classification.config>] [-S <msg-msg.map>]
                  [-G <gen-msg.map>] [--snort-conf <snort.conf>]
                  [--directory <spool directory>] [--prefix <spool file prefix>]
                  [--bookmark] [--follow] [--delete] [--output <filename>]
                  [--stdout]
                  [filenames [filenames ...]]

    positional arguments:
      filenames

    optional arguments:
      -h, --help            show this help message and exit
      -C <classification.config>
                            path to classification config
      -S <msg-msg.map>      path to sid-msg.map
      -G <gen-msg.map>      path to gen-msg.map
      --snort-conf <snort.conf>
                            attempt to load classifications and map files based on
                            the location of the snort.conf
      --directory <spool directory>
                            spool directory (eg: /var/log/snort)
      --prefix <spool file prefix>
                            spool filename prefix (eg: unified2.log)
      --bookmark            enable bookmarking
      --follow              follow files/continuous mode (spool mode only)
      --delete              delete spool files
      --output <filename>   output filename (eg: /var/log/snort/alerts.json
      --stdout              also log to stdout if --output is a file

    If --directory and --prefix are provided files will be read from
    the specified 'spool' directory. Otherwise files on the command
    line will be processed.

An alternative to using command line arguments is to put the arguments
in a file and call u2json like::

    u2json @filename

where filename looks something like::

    -C=/etc/snort/etc/classification.config
    -S=/etc/snort/etc/sid-msg.map
    -G=/etc/snort/etc/gen-msg.map
    --directory=/var/log/snort
    --prefix=unified2.log
    --output=/var/log/snort/alerts.json
    --follow
    --bookmark
    --delete

"""

from __future__ import print_function

import sys
import os
import os.path

if sys.argv[0] == __file__:
    sys.path.insert(
        0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import socket
import time
import json
import logging
from datetime import datetime
try:
    from collections import OrderedDict
except ImportError as err:
    from idstools.compat.ordereddict import OrderedDict

try:
    import argparse
except ImportError as err:
    from idstools.compat.argparse import argparse

from idstools import unified2
from idstools import maps

logging.basicConfig(level=logging.INFO, format="%(message)s")
LOG = logging.getLogger()

proto_map = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
}

def get_tzoffset(sec):
    offset = datetime.fromtimestamp(sec) - datetime.utcfromtimestamp(sec)
    if offset.days == -1:
        return "-%02d%02d" % (
            (86400 - offset.seconds) / 3600, (86400 - offset.seconds) % 3600)
    else:
        return "+%02d%02d" % (
            offset.seconds / 3600, offset.seconds % 3600)

def render_timestamp(sec, usec):
    tt = time.localtime(sec)
    return "%04d-%02d-%02dT%02d:%02d:%02d.%06d%s" % (
        tt.tm_year, tt.tm_mon, tt.tm_mday, tt.tm_hour, tt.tm_min, tt.tm_sec, 
        usec, get_tzoffset(sec))

class SuricataJsonFilter(object):

    def __init__(self, msgmap=None, classmap=None):
        self.msgmap = msgmap
        self.classmap = classmap

    def filter(self, event):
        output = OrderedDict()
        output["timestamp"] = render_timestamp(
            event["event-second"], event["event-microsecond"])
        output["event_type"] = "alert"
        output["src_ip"] = event["source-ip"]
        if event["protocol"] in [socket.IPPROTO_UDP, socket.IPPROTO_TCP]:
            output["src_port"] = event["sport-itype"]
        output["dest_ip"] = event["destination-ip"]
        if event["protocol"] in [socket.IPPROTO_UDP, socket.IPPROTO_TCP]:
            output["dest_port"] = event["dport-icode"]
        output["proto"] = self.getprotobynumber(event["protocol"])

        if event["protocol"] in [socket.IPPROTO_ICMP, socket.IPPROTO_ICMPV6]:
            output["icmp_type"] = event["sport-itype"]
            output["icmp_code"] = event["dport-icode"]

        alert = OrderedDict()
        alert["action"] = "blocked" if event["blocked"] == 1 else "allowed"
        alert["gid"] = event["generator-id"]
        alert["signature_id"] = event["signature-id"]
        alert["rev"] = event["signature-revision"]
        alert["signature"] = self.resolve_msg(event)
        alert["category"] = self.resolve_classification(event)
        alert["severity"] = event["priority"]
        output["alert"] = alert

        return output

    def resolve_classification(self, event, default=None):
        if self.classmap:
            classinfo = self.classmap.get(event["classification-id"])
            if classinfo:
                return classinfo["description"]
        return default

    def resolve_msg(self, event, default=None):
        if self.msgmap:
            signature = self.msgmap.get(
                event["generator-id"], event["signature-id"])
            if signature:
                return signature["msg"]
        return default

    def getprotobynumber(self, protocol):
        return proto_map.get(protocol, str(protocol))

class OutputWrapper(object):

    def __init__(self, filename, fileobj=None):
        self.filename = filename
        self.fileobj = fileobj

        if self.fileobj is None:
            self.reopen()
            self.isfile = True
        else:
            self.isfile = False

    def reopen(self):
        if self.fileobj:
            self.fileobj.close()
        self.fileobj = open(self.filename, "ab")

    def write(self, buf):
        if self.isfile:
            if not os.path.exists(self.filename):
                self.reopen()
        self.fileobj.write(buf)
        self.fileobj.write("\n")
        self.fileobj.flush()

def load_from_snort_conf(snort_conf, classmap, msgmap):
    snort_etc = os.path.dirname(os.path.expanduser(snort_conf))

    classification_config = os.path.join(snort_etc, "classification.config")
    if os.path.exists(classification_config):
        LOG.debug("Loading %s.", classification_config)
        classmap.load_from_file(open(classification_config))

    genmsg_map = os.path.join(snort_etc, "gen-msg.map")
    if os.path.exists(genmsg_map):
        LOG.debug("Loading %s.", genmsg_map)
        msgmap.load_generator_map(open(genmsg_map))

    sidmsg_map = os.path.join(snort_etc, "sid-msg.map")
    if os.path.exists(sidmsg_map):
        LOG.debug("Loading %s.", sidmsg_map)
        msgmap.load_signature_map(open(sidmsg_map))

epilog = """If --directory and --prefix are provided files will be
read from the specified 'spool' directory.  Otherwise files on the
command line will be processed.
"""

def main():

    msgmap = maps.SignatureMap()
    classmap = maps.ClassificationMap()

    parser = argparse.ArgumentParser(
        fromfile_prefix_chars='@', epilog=epilog)
    parser.add_argument(
        "-C", dest="classification_path", metavar="<classification.config>", 
        help="path to classification config")
    parser.add_argument(
        "-S", dest="sidmsgmap_path", metavar="<msg-msg.map>", 
        help="path to sid-msg.map")
    parser.add_argument(
        "-G", dest="genmsgmap_path", metavar="<gen-msg.map>", 
        help="path to gen-msg.map")
    parser.add_argument(
        "--snort-conf", dest="snort_conf", metavar="<snort.conf>",
        help="attempt to load classifications and map files based on the "
        "location of the snort.conf")
    parser.add_argument(
        "--directory", metavar="<spool directory>",
        help="spool directory (eg: /var/log/snort)")
    parser.add_argument(
        "--prefix", metavar="<spool file prefix>",
        help="spool filename prefix (eg: unified2.log)")
    parser.add_argument(
        "--bookmark", action="store_true", default=False,
        help="enable bookmarking")
    parser.add_argument(
        "--follow", action="store_true", default=False,
        help="follow files/continuous mode (spool mode only)")
    parser.add_argument(
        "--delete", action="store_true", default=False,
        help="delete spool files")
    parser.add_argument(
        "--output", metavar="<filename>",
        help="output filename (eg: /var/log/snort/alerts.json")
    parser.add_argument(
        "--stdout", action="store_true", default=False,
        help="also log to stdout if --output is a file")
    parser.add_argument(
        "filenames", nargs="*")
    args = parser.parse_args()

    if args.snort_conf:
        load_from_snort_conf(args.snort_conf, classmap, msgmap)

    if args.classification_path:
        classmap.load_from_file(
            open(os.path.expanduser(args.classification_path)))
    if args.genmsgmap_path:
        msgmap.load_generator_map(open(os.path.expanduser(args.genmsgmap_path)))
    if args.sidmsgmap_path:
        msgmap.load_signature_map(open(os.path.expanduser(args.sidmsgmap_path)))

    if msgmap.size() == 0:
        LOG.warn("WARNING: No alert message map entries loaded.")
    else:
        LOG.info("Loaded %s rule message map entries.", msgmap.size())

    if classmap.size() == 0:
        LOG.warn("WARNING: No classifications loaded.")
    else:
        LOG.info("Loaded %s classifications.", classmap.size())

    output_filter = SuricataJsonFilter(msgmap, classmap)
    if args.output:
        output = OutputWrapper(args.output)
    else:
        output = OutputWrapper("-", sys.stdout)

    if args.directory and args.prefix:
        reader = unified2.SpoolEventReader(
            directory=args.directory,
            prefix=args.prefix,
            follow=args.follow,
            delete=args.delete,
            bookmark=args.bookmark)

        for event in reader:
            encoded = json.dumps(output_filter.filter(event))
            output.write(encoded)
            if output.isfile and args.stdout:
                print(encoded)

    elif args.filenames:
        reader = unified2.FileEventReader(*args.filenames)
        for event in reader:
            print(json.dumps(output_filter.filter(event)))

    else:
        print("nothing to do.")

if __name__ == "__main__":
    sys.exit(main())
