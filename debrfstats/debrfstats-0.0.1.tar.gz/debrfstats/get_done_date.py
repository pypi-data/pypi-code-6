#!/usr/bin/env python

# Copyright: 2014 Dariusz Dwornikowski <dariusz.dwornikowski@cs.put.poznan.pl>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
from datetime import datetime
import mailbox
import re
import os
import tempfile


def get_done_date(bug_num, nocache=False):

    CACHE_DIR = os.path.expanduser("~") + "/.cache/rfs_bugs/"

    def get_from_cache():
        if os.path.exists("{}{}".format(CACHE_DIR, bug_num)):
            with open("{}{}".format(CACHE_DIR, bug_num)) as f:
                return datetime.strptime(f.readlines()[0].rstrip(), "%Y-%m-%d").date()
        else:
            return None
    done_date = None
    if not nocache:
        done_date = get_from_cache()

    def try_body(text):
        reg = "\(at\s.+\)\s+by\sbugs\.debian\.org;\s(\d{1,2}\s\w\w\w\s\d\d\d\d)"
        handle, name = tempfile.mkstemp()
        with open(name, "w") as f:
            f.write(text.encode('latin-1'))
        mbox = mailbox.mbox(name)
        for i in mbox.items():
            if i[1].is_multipart():
                for m in i[1].get_payload():
                    if "close {}".format(bug_num) in str(m):
                        try:
                            result = re.search(reg, i[1]['Received'])
                            return datetime.strptime(result.group(1), "%d %b %Y")
                        except:
                            return None
            else:
                if "close {}".format(bug_num) in i[1].get_payload():
                    try:
                        result = re.search(reg, i[1]['Received'])
                        return datetime.strptime(result.group(1), "%d %b %Y")
                    except:
                        return None
        return None

    def try_header(text):
        reg = "Received:\s\(at\s\d\d\d\d\d\d-(close|done)\)\s+by.+"
        try:
            result = re.search(reg, r.text)
            line = result.group(0)
            reg2 = "\d{1,2}\s\w\w\w\s\d\d\d\d"
            result = re.search(reg2, line)
            d = datetime.strptime(result.group(0), "%d %b %Y")
            return d
        except:
            return None

    def try_cc(text):
        reg = "\(at\s.+\)\s+by\sbugs\.debian\.org;\s(\d{1,2}\s\w\w\w\s\d\d\d\d)"
        handle, name = tempfile.mkstemp()
        with open(name, "w") as f:
            f.write(text.encode('latin-1'))
        mbox = mailbox.mbox(name)
        for i in mbox.items():
            if ('CC' in i[1] and "done" in i[1]['CC']) or ('To' in i[1] and "done" in i[1]['To']):
                try:
                    result = re.search(reg, i[1]['Received'])
                    return datetime.strptime(result.group(1), "%d %b %Y")
                except:
                    return None

    if done_date is not None:
        return done_date
    else:
        r = requests.get("https://bugs.debian.org/cgi-bin/bugreport.cgi?mbox=yes;bug={};mboxstatus=yes".format(bug_num))
        d = try_header(r.text)
        if d is None:
            d = try_cc(r.text)
        if d is None:
            d = try_body(r.text)
        if d is not None:
            with open("{}{}".format(CACHE_DIR, bug_num), "w") as f:
                f.write("{}".format(d.date()))
        else:
            if os.path.exists("{}{}".format(CACHE_DIR, bug_num)):
                os.remove("{}{}".format(CACHE_DIR, bug_num))
            return None
        return d.date()

if __name__ == "__main__":
    print get_done_date(752210)
