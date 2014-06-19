#!/usr/bin/env python
#
# Copyright 2014 NGENIX
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import os
import time
import urllib2, base64
import json
import sys

BRAILLE_OFFSET = 0x2800

LINES_MAP = (
    (0x00, 0x80, 0xa0, 0xb0, 0xb8),
    (0x40, 0xc0, 0xe0, 0xf0, 0xf8),
    (0x44, 0xc4, 0xe4, 0xf4, 0xfc),
    (0x46, 0xc6, 0xe6, 0xf6, 0xfe),
    (0x47, 0xc7, 0xe7, 0xf7, 0xff),
    )

DIMENSIONS = (('b', 1),
              ('K', 1e3),
              ('M', 1e6),
              ('G', 1e9),
              ('T', 1e12))

HOR = unichr(0x2500)
VERT = unichr(0x2502)
CROSS = unichr(0x253C)


# http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
def getTerminalSize():
    """Returns terminal width, height
    """
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass

    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])


class Graph(object):
    height = 25
    max_points = height * 4

    def __init__(self, data):
        self.data = data

    def draw(self):
        self._max = max(x[1] for x in self.data)
        self._normalized = [self.normalize(self._max, x[1]) for x in self.data]
        self._dim_l, self._dim_n = self.dimension(self._max)
        for i in xrange(0, self.height):
            self.draw_line(i)
        self.draw_timeline()

    def dimension(self, max_):
        i = 0
        while (max_ / DIMENSIONS[i][1] > 1e3):
            i += 1
        return DIMENSIONS[i]

    def normalize(self, max_, point):
        return int(point / max_ * self.max_points)

    def points_for_line(self, line, count):
        t = count - (self.height - line - 1) * 4
        if t < 0:
            return 0
        elif t > 4:
            return 4
        else:
            return t

    def trim_num(self, num):
        res = str(num)[0:4]
        if res.endswith('.'):
            res = ' ' + res[:-1]
        return res

    def draw_line(self, line):
        buf = list()
        if line % 5 == 0:
            buf.append(self.trim_num(self._max / self._dim_n * float(self.height - line) / self.height))
        else:
            buf.append('    ')
        buf.append(self._dim_l if line == 0 else VERT)
        for i in xrange(0, len(self._normalized) / 2):
            p1, p2 = (self.points_for_line(line, self._normalized[i * 2]),
                      self.points_for_line(line, self._normalized[i * 2 + 1]))
            buf.append(unichr(BRAILLE_OFFSET + LINES_MAP[p1][p2]))
        print ''.join(buf)

    def draw_timeline(self):
        buf = list()
        buf.append('   0' + CROSS)
        l = len(self._normalized) / 2
        remains = l
        while remains >= 5:
            buf.append(HOR * 2 + CROSS + HOR * 2)
            remains -= 5
            if remains >= 4:
                buf.append(HOR * 4)
                remains -= 4
        buf.append(HOR * remains)
        print ''.join(buf)

        buf = list()
        buf.append('     ')
        remains = l
        while remains >= 5:
            t = time.localtime(self.data[(l - remains + 6) * 2][0])
            buf.append("{0:02}:{1:02}".format(t.tm_hour, t.tm_min))
            remains -= 5
            if remains >= 4:
                buf.append(' ' * 4)
                remains -= 4
        print ''.join(buf)


def read_config():
    config_file = os.path.join(os.environ['HOME'], '.hackergraph')
    if not os.path.isfile(config_file):
        sys.stderr.write("Config file not found ({0})\n".format(config_file))
        sys.exit(1)
    with open(config_file) as f:
        config = json.load(f)
    if 'user' not in config or 'token' not in config:
        sys.stderr.write("Please set up 'user' and 'token' in config file")
        sys.exit(1)
    return config


def usage():
    sys.stderr.write("Usage: {0} <target>\n".format(sys.argv[0]))
    sys.stderr.write("(you can also set up default target in config file)\n")


def main():
    config = read_config()
    if len(sys.argv) < 2:
        target = config.get('target', None)
    else:
        target = sys.argv[1]

    if target is None:
        usage()
        return 1

    try:
        int(target)
        url = "https://api.ngenix.net/v1/reports/traffic_total/{0}/location/_all".format(target)
    except ValueError:
        url = "https://api.ngenix.net/v1/reports/traffic/{0}/location/_all".format(target)
    w, h = getTerminalSize()
    if w < 149:
        url += '?res=600'

    request = urllib2.Request(url)
    base64string = base64.encodestring("{0}/token:{1}".format(config['user'], config['token'])).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    try:
        result = urllib2.urlopen(request)
        js = json.load(result)
    except urllib2.HTTPError as e:
        sys.stderr.write("Could not fetch data, error code: {0}\n".format(e.code))
        return 1

    result.close()
    Graph(js['avg']).draw()
    return 0

if __name__ == '__main__':
    sys.exit(main())
