# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import with_statement, division, print_function
import chardet
import re
import codecs

import ox


__all__ = []


def _detect_encoding(fp):
    bomDict={ # bytepattern : name
              (0x00, 0x00, 0xFE, 0xFF): "utf_32_be",
              (0xFF, 0xFE, 0x00, 0x00): "utf_32_le",
              (0xFE, 0xFF, None, None): "utf_16_be",
              (0xFF, 0xFE, None, None): "utf_16_le",
              (0xEF, 0xBB, 0xBF, None): "utf_8",
            }

    # go to beginning of file and get the first 4 bytes
    oldFP = fp.tell()
    fp.seek(0)
    (byte1, byte2, byte3, byte4) = tuple(map(ord, fp.read(4)))

    # try bom detection using 4 bytes, 3 bytes, or 2 bytes
    bomDetection = bomDict.get((byte1, byte2, byte3, byte4))
    if not bomDetection:
        bomDetection = bomDict.get((byte1, byte2, byte3, None))
        if not bomDetection:
            bomDetection = bomDict.get((byte1, byte2, None, None))
    ## if BOM detected, we're done :-)
    fp.seek(oldFP)
    if bomDetection:
        return bomDetection
    encoding = 'latin-1'
    #more character detecting magick using http://chardet.feedparser.org/
    fp.seek(0)
    rawdata = fp.read()
    #if data can be decoded as utf-8 use that, try chardet otherwise
    #chardet detects utf-8 as ISO-8859-2 most of the time
    try:
        data = unicode(rawdata, 'utf-8')
        encoding = 'utf-8'
    except:
        encoding = chardet.detect(rawdata)['encoding']
    fp.seek(oldFP)
    return encoding


def load(filename, offset=0):
    '''
        filename path to an srt file
        offset in seconds shift all in/out points by offset

        returns list with objects that have in,out,value and id
    '''
    srt = []

    def parse_time(t):
        return offset + ox.time2ms(t.replace(',', '.')) / 1000

    with open(filename) as f:
        encoding = _detect_encoding(f)
        data = f.read()
    try:
        data = unicode(data, encoding)
    except:
        try:
            data = unicode(data, 'latin-1')
        except:
            print("failed to detect encoding, giving up")
            return srt

    data = data.replace('\r\n', '\n')
    srts = re.compile('(\d\d:\d\d:\d\d[,.]\d\d\d)\s*?-->\s*?(\d\d:\d\d:\d\d[,.]\d\d\d).*?\n(.*?)\n\n', re.DOTALL)
    i = 0
    for s in srts.findall(data):
        _s = {'id': str(i),
              'in': parse_time(s[0]),
              'out': parse_time(s[1]),
              'value': s[2].strip()
        }
        srt.append(_s)
        i += 1
    return srt

def encode(data):
    '''
        encodes list of objects with in,out,value into srt
        result is utf-8 encoded bytestring
    '''
    srt = u''
    i = 1
    for s in data:
        srt += '%d\r\n%s --> %s\r\n%s\r\n\r\n' % (
            i,
            ox.format_duration(s['in']*1000, years=False).replace('.', ','),
            ox.format_duration(s['out']*1000, years=False).replace('.', ','),
            s['value'].replace('\n', '\r\n').strip()
        )
        i += 1
    return codecs.BOM_UTF8 + srt.encode('utf-8')

