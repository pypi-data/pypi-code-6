from lacore.log import getLogger
from lacore.adf.elements import Links
from lacore.archive.urls import UrlArchiver
from lacore.archive.stream import StreamArchiver
from lacore.storage.s3 import S3Connection
from . import Dumper
from StringIO import StringIO


class BaseS3Dumper(Dumper):

    def __init__(self, key=None, retries=4, connection=None, **kwargs):
        if 'chunk' not in kwargs:
            kwargs['chunk'] = 10 * 1024 ** 2
        elif kwargs['chunk'] < 5242880:
            raise ValueError("S3Dumper chunk must be at least 5242880")
        super(BaseS3Dumper, self).__init__(**kwargs)
        self.connection = connection
        self.key = key
        if self.connection is None:
            self.connection = S3Connection()
        self.etags = []
        self.retries = retries
        self.seq = 0
        self.upload = None

    def update(self, result):
        super(BaseS3Dumper, self).update(result)
        if 'links' not in self.docs:
            self.docs['links'] = Links()
        if self.upload is not None:
            key = self.connection.complete_multipart(self.upload, self.etags)
            self.docs['links'].upload = (key.key_name, key.etag)

    @property
    def bucket(self):
        return self.connection.getbucket()

    def write(self, data):
        sz = len(data)
        fp = StringIO(data)
        for attempt in range(self.retries):
            fp.seek(0)
            getLogger().debug("attempt %d/%d to transfer part %d",
                              attempt, self.retries, self.seq)

            try:
                key = self.upload.upload_part_from_file(
                    fp=fp,
                    part_num=self.seq+1,
                    size=sz
                )
                getLogger().debug("succesfully uploaded part %d: %s",
                                  self.seq, key)
                self.seq += 1
                self.etags.append(key.etag)
                break
            except Exception as exc:
                getLogger().debug("exception while uploading part %d",
                                  self.seq, exc_info=True)

                if attempt == self.retries-1:
                    raise exc

    def __enter__(self):
        if self.upload is None:
            self.upload = self.connection.newupload(self.key)
        return self

    def __exit__(self, eType, eValue, eTrace):
        super(BaseS3Dumper, self).__exit__(eType, eValue, eTrace)
        if eType is not None:
            getLogger().debug("cancelling upload..", exc_info=True)
            if self.upload is not None:
                self.upload.cancel_upload()


class S3Dumper(BaseS3Dumper, UrlArchiver):
    pass


class S3StreamDumper(BaseS3Dumper, StreamArchiver):
    pass
