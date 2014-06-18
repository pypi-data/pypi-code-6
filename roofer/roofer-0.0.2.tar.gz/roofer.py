#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
Copyright 2014 by Franck Barbenoire <contact@franck-barbenoire.fr>

This program is based on this article from Daniel Gasienica :
    http://www.gasi.ch/blog/inside-deep-zoom-2/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

from io import BytesIO
import math
from multiprocessing import Lock, Queue
import os
from PIL import Image
from threading import Thread
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from xml.dom import minidom
#import pdb; pdb.set_trace()

__version__ = '0.0.2'

class Roofer(object):
    def __init__(self, xml_url, dir_suffix='_files', mode='RGB'):
        """Initializes attributes from xml image definition"""
        try:
            response = urlopen(xml_url)
            xmldoc = minidom.parseString(response.read())
            image_item = xmldoc.getElementsByTagName('Image')
            self._format = image_item[0].attributes['Format'].value
            self._overlap = int(image_item[0].attributes['Overlap'].value)
            self._tile_size = int(image_item[0].attributes['TileSize'].value)
            size_item = xmldoc.getElementsByTagName('Size')
            self._width = int(size_item[0].attributes['Width'].value)
            self._height = int(size_item[0].attributes['Height'].value)
        except:
            raise Exception('problem while parsing xml file %s' % (xml_url,))

        self._dir_base = os.path.splitext(xml_url)[0]
        self._dir_suffix = dir_suffix
        self._mode = mode

        self._levels = {}
        self._max_level = self._get_maximum_level(self._width, self._height)
        self._compute_levels(self._width, self._height, self._tile_size)
        return

    def _get_maximum_level(self, width, height):
        """Computes the maximum level"""
        return int(math.ceil(math.log(float(max(self._width, self._height)), 2)))

    def _compute_levels(self, width, height, tile_size):
        """Computes the sizes and tile numbers for all levels"""
        for level in range(self._max_level, -1, -1):
            # compute number of rows & columns
            tile_size = float(tile_size)
            columns = int(math.ceil(width / tile_size))
            rows = int(math.ceil(height / tile_size))

            self._levels[level] = (width, height, columns, rows)

            # compute dimensions of next level
            width = int(math.ceil(width / 2.0))
            height = int(math.ceil(height / 2.0))

        return

    def _get_tile_url(self, level, column, row):
        """Returns a tile url given by its level, column and row"""
        return os.path.join('%s%s' % (self._dir_base, self._dir_suffix),
                            '%d' % (level,),
                            '%d_%d.%s' % (column, row, self._format))

    def _get_tile_position(self, level, column, row):
        """Returns the position of a tile given by its level, column and row"""
        offset_y = self._overlap if row != 0 else 0
        offset_x = self._overlap if column != 0 else 0
        x = column*self._tile_size - offset_x
        y = row*self._tile_size - offset_y
        return x, y

    @property
    def maximum_level(self):
        """Returns the maximim level"""
        return self._max_level

    def image_size(self, level):
        """Returns the image size of a level"""
        if not 0 <= level <= self._max_level:
            return -1, -1
        return self._levels[level][0], self._levels[level][1]

    def get_level_size(self, level):
        """Returns a tuple (width, height, columns, rows) for a level"""
        if not 0 <= level <= self._max_level:
            return
        return self._levels[level]

    def get_tile_image(self, level, column, row):
        """Returns a tile image from a level at given coordinates"""
        if not 0 <= level <= self._max_level:
            return
        if not 0 <= column < self._levels[level][2] or \
           not 0 <= row < self._levels[level][3]:
            return
        img_url = self._get_tile_url(level, column, row)
        reponse = urlopen(img_url)
        return Image.open(BytesIO(reponse.read()))

    def get_level_image(self, level):
        """Builds and returns the whole image corresponding to a level"""
        if not 0 <= level <= self._max_level:
            return
        width, height, columns, rows = self._levels[level]
        try:
            full_img = Image.new(self._mode, (width, height))
        except:
            return
        for c in range(columns):
            for r in range(rows):
                x, y = self._get_tile_position(level, c, r)
                try:
                    img_url = self._get_tile_url(level, c, r)
                    reponse = urlopen(img_url)
                    img = Image.open(BytesIO(reponse.read()))
                except:
                    print('%s not found' % (img_url,))
                    return
                full_img.paste(img, (x, y))
        return full_img

    def get_level_image_t(self, level, tasks=2):
        """Builds and returns the whole image corresponding to a level"""

        def _get_image_and_paste():
            for cr in iter(tile_queue.get, 'STOP'):
                c, r = eval(cr)
                offset_y = self._overlap if r != 0 else 0
                offset_x = self._overlap if c != 0 else 0
                x = c*self._tile_size - offset_x
                y = r*self._tile_size - offset_y
                try:
                    img_url = os.path.join('%s%s' % (self._dir_base,
                                                     self._dir_suffix),
                                           '%d' % (level,),
                                           '%d_%d.%s' % (c, r, self._format))
                    reponse = urlopen(img_url)
                    i = Image.open(BytesIO(reponse.read()))
                except:
                    return
                image_lock.acquire()
                try:
                    full_img.paste(i, (x, y))
                finally:
                    image_lock.release()
            return

        if not 0 <= level <= self._max_level:
            return
        width, height, columns, rows = self._levels[level]
        try:
            full_img = Image.new(self._mode, (width, height))
        except:
            return
        tile_queue = Queue()
        image_lock = Lock()
        for c in range(columns):
            for r in range(rows):
                tile_queue.put(str((c, r)))
        for _ in range(tasks):
            tile_queue.put('STOP')
        threads = []
        # Start all threads
        for _ in range(tasks):
            t = Thread(target=_get_image_and_paste, args=())
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return full_img

if __name__ == "__main__":
    # when invoked as main, assembles the tiled images to a full image

    try:
        input = raw_input
    except NameError:
        pass

    import argparse
    try:
        from urllib.parse import urlparse
    except:
        from urlparse import urlparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', type=int, default=-1)
    parser.add_argument('infile', help='Input directory or url')
    parser.add_argument('outfile', help='Output image file')
    args = parser.parse_args()

    input_file = args.infile
    if urlparse(input_file).scheme == '':
        input_file = 'file://' + input_file

    roofer = Roofer(input_file, dir_suffix='')

    max_level = roofer.maximum_level
    if args.level == -1:
        level = max_level
    else:
        if args.level > max_level:
            level = max_level
        else:
            level = args.level
    image_size = roofer.image_size(level)
    print('image size : width = %d, height = %d' % image_size)
    img = roofer.get_level_image_t(max_level)
    if img:
        img.save(args.outfile)
