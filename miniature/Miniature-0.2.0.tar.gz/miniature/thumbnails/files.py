# -*- coding: utf-8 -*-
#
# This file is part of Miniature released under the FreeBSD license.
# See the LICENSE for more information.
from __future__ import (print_function, division, absolute_import, unicode_literals)


class ImageFile(object):
    def __init__(self, storage, name,):
        self.storage = storage
        self.name = name

    def __unicode__(self):
        return self.name

    @property
    def url(self):
        return self.storage.url(self.name)
