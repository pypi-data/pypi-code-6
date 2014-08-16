# -*- coding: utf-8 -*-
#
# This file is part of Miniature released under the FreeBSD license.
# See the LICENSE for more information.
from __future__ import (print_function, division, absolute_import, unicode_literals)

import hashlib
import os.path

from django.core import cache as cache_
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.utils.encoding import force_bytes
from django.utils.functional import LazyObject
from django.utils.six.moves.urllib.parse import urljoin

from miniature.processor import get_processor
from miniature.thumbnails.conf import settings
from miniature.thumbnails.files import ImageFile

try:
    cache = cache_.get_cache(settings.MINIATURE_CACHE)
except cache_.InvalidCacheBackendError:
    cache = cache_.cache


class ThumbnailStorage(LazyObject):
    def _setup(self):
        base_path = os.path.join(settings.MEDIA_ROOT, settings.MINIATURE_THUMB_PATH)
        base_url = urljoin(settings.MEDIA_URL, settings.MINIATURE_THUMB_URL)
        self._wrapped = get_storage_class()(location=base_path, base_url=base_url)

storage = ThumbnailStorage()

Processor = get_processor(settings.MINIATURE_PROCESSOR)


def get_thumbnail(image, operations):
    op_id = hashlib.md5(force_bytes(repr(operations))).hexdigest()
    entries = cache.get(image.path)
    if entries is None:
        entries = {}

    cached_path = entries.get(op_id)
    if cached_path is not None and not storage.exists(cached_path):
        # Something in cache but not files, drop entry
        del entries[op_id]
        cached_path = None

    if not cached_path:
        img_id = hashlib.md5(force_bytes('{0}{1}'.format(image.path, repr(operations)))).hexdigest()
        # Create thumbnail
        dest_file = ContentFile('')
        with Processor(image) as p:
            p.operations(*operations).save(dest_file)

            cached_path = '{0}.{1}'.format(os.path.join(img_id[0:2], img_id[2:4], img_id), p.format)
            storage.save(cached_path, dest_file)
            del dest_file

    entries[op_id] = cached_path
    cache.set(image.path, entries)
    return ImageFile(storage, cached_path)
