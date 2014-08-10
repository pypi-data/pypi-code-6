from __future__ import absolute_import

from .base import Remote
from ubackup import settings, utils
from ubackup.utils import filesizeformat, stream_shell
from datetime import datetime

import requests
import sys

import logging
logger = logging.getLogger(__name__)


class DropboxRemote(Remote):
    TYPE = "dropbox"

    def __init__(self, token):
        self.token = token

    def sign(self):
        return {"Authorization": "Bearer %s" % self.token}

    def request(self, method, url, *args, **kwargs):
        return requests.request(
            method,
            "%s/%s" % (settings.DROPBOX_CONTENT_URL, url),
            *args,
            **dict(kwargs, headers=self.sign()))

    def push(self, stream, file_name):
        logger.info('Start pushing %s' % file_name)
        start = datetime.now()

        chunk = stream.read(settings.CHUNK_SIZE)
        r = self.request(
            method="put",
            url="chunked_upload",
            data=chunk)
        data = r.json()
        upload_id = data.get("upload_id")
        offset = data.get("offset")
        logger.info('Pushed: %s' % filesizeformat(sys.getsizeof(chunk)))

        while True:
            chunk = stream.read(settings.CHUNK_SIZE)
            if not chunk:
                break

            r = self.request(
                method="put",
                url="chunked_upload",
                params={
                    "upload_id": upload_id,
                    "offset": offset
                },
                data=chunk)
            data = r.json()
            offset = data.get("offset")

            logger.info('Pushed: %s' % filesizeformat(sys.getsizeof(chunk)))

        r = self.request(
            method="post",
            url="commit_chunked_upload/sandbox/%s" % file_name,
            params={
                "upload_id": upload_id,
                "overwrite": True,
            })

        logger.info('Pushed: done in %ss' % utils.total_seconds(datetime.now() - start))

    def pull(self, file_name):
        header = 'Authorization: %s' % self.sign()['Authorization']
        return stream_shell(
            cmd='wget -qO- --header="%s" %s/files/sandbox/%s' % (header, settings.DROPBOX_CONTENT_URL, file_name))
