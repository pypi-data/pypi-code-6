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

from os.path import join
from tumulus import tags as t, formulas as f, lib

from druid.image import Image

__all__ = ('Druid', )


class Druid:

    def __init__(
            self,
            local_static='static',
            public_static='/static',
            image_prefix='img',
            thumb_prefix='thumb',
            ):
        self.local_static = local_static
        self.public_static = public_static
        self.image_prefix = image_prefix
        self.thumb_prefix = thumb_prefix

    @property
    def image_dir(self):
        return join(
            self.local_static,
            self.image_prefix,
            )

    def page(self, *args, **kwargs):
        return t.html(
            t.head(
                f.utf8(),
                ),
            t.body(*args, **kwargs),
            )

    def image(self, path, alt=''):
        return Image(self, path, alt)
