 # -*- coding: utf-8 -*-

# This file is part of Druid.
#
# Copyright (C) 2014 OKso (http://okso.me)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os.path import join, isfile, splitext
from tumulus import tags as t, formulas as f, lib
from PIL import Image as PIL_Image

__all__ = ('Thumbnail', 'Image')


class Thumbnail:

    def __init__(self, image, size):
        self.image = image
        self.size = size
        prefix, ext = splitext(image.path)
        self.path = '{}-{}x{}{}'.format(
            prefix, self.size[0], self.size[1], ext)
        self.save()

    def soup(self):
        return t.img(
            src=join(
                self.image.druid.public_static,
                self.image.druid.thumb_prefix,
                self.path,
                ),
            alt=self.image.alt,
            ).soup()

    def build(self):
        return self.soup().prettify()

    def file_path(self):
        return join(
            self.image.druid.local_static,
            self.image.druid.thumb_prefix,
            self.path,
            )

    def save(self, force=False):
        if not isfile(self.file_path()) or force:
            img = PIL_Image.open(self.image.file_path())
            out = img.resize(self.size)
            out.save(self.file_path())

    def file(self, mode='rb'):
        return open(
            self.file_path(),
            mode=mode,
            )


class Image:

    def __init__(self, druid, path, alt):
        self.druid = druid
        self.path = path
        self.alt = alt

    def soup(self):
        return t.img(
            src=join(
                self.druid.public_static,
                self.druid.image_prefix,
                self.path,
                ),
            alt=self.alt,
            ).soup()

    def build(self):
        return self.soup().prettify()

    def file_dir(self):
        return join(
            self.druid.local_static,
            self.druid.image_prefix,
            )

    def file_path(self):
        return join(
            self.file_dir(),
            self.path
            )

    def file(self, mode='rb'):
        return open(
            self.file_path(),
            mode=mode,
            )

    def thumb(self, size):
        return Thumbnail(self, size)