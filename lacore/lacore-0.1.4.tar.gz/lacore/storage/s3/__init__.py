import os
import hashlib

from .. import StorageConnection
from lacore.date import parse_timestamp, remaining_time
from lacore.log import getLogger
from lacore.decorators import cached_property
from lacore.exceptions import UploadInvalidError
from boto import connect_s3
from boto.s3.key import Key
from boto.s3.connection import NoHostProvided
from boto.regioninfo import get_regions


class S3Connection(StorageConnection):
    def __init__(self, token_access_key=None, token_secret_key=None,
                 token_session=None, token_expiration=None, bucket=None,
                 prefix='', port=None, host=NoHostProvided,
                 **kwargs):
        super(S3Connection, self).__init__(**kwargs)
        self.accesskey = token_access_key
        self.secret = token_secret_key
        self.sectoken = token_session
        self.expires = token_expiration
        self._bucket = bucket
        self.prefix = prefix
        self.conn = None
        self.port = port
        if self.port is None:
            port = os.environ.get('S3_PORT')
            self.port = int(port) if port is not None else None
        self.host = host
        if self.host is NoHostProvided:
            host = os.environ.get('S3_HOST')
            s3_region = os.environ.get('S3_REGION')
            if host is None and s3_region is not None:
                for region in get_regions('s3'):
                    if region.name == s3_region:
                        self.host = region.endpoint

    def getconnection(self):
        if self.conn is None:
            self.conn = connect_s3(
                aws_access_key_id=self.accesskey,
                aws_secret_access_key=self.secret,
                security_token=self.sectoken,
                host=self.host,
                port=self.port)
        return self.conn

    @cached_property
    def bucket(self):
        return self.getconnection().get_bucket(self._bucket)

    def newkey(self, key):
        return Key(self.bucket, self.prefix + key)

    def __getstate__(self):
        """ prepare the object for pickling. """
        state = self.__dict__
        state['conn'] = None
        return state

    def newupload(self, key):
        return self.bucket.initiate_multipart_upload(self.prefix + key)

    def getupload(self, uid):
        for upload in self.bucket.get_all_multipart_uploads():
            if uid == upload.id:
                return upload

    def complete_multipart(self, upload, etags):
        xml = '<CompleteMultipartUpload>\n'
        md5 = hashlib.md5()
        for seq, etag in enumerate(etags):
            xml += '  <Part>\n'
            xml += '    <PartNumber>{}</PartNumber>\n'.format(seq+1)
            xml += '    <ETag>{}</ETag>\n'.format(etag)
            xml += '  </Part>\n'
            md5.update(etag.replace('"', '').decode("hex"))
        xml += '</CompleteMultipartUpload>'
        key = self.bucket.complete_multipart_upload(
            upload.key_name, upload.id, xml)
        if key.etag != '"{0}-{1}"'.format(md5.hexdigest(), len(etags)):
            raise UploadInvalidError("the multipart key had an invalid eTag")
        return key


class MPConnection(S3Connection):
    def __init__(self, token_expiration=None, grace=120, **kwargs):
        super(MPConnection, self).__init__(**kwargs)
        self.grace = grace
        self.conn = None
        self.expiration = None
        if token_expiration is not None:
            try:
                self.expiration = parse_timestamp(token_expiration)
            except ValueError:
                getLogger().debug("invalid token expiration: %s",
                                  token_expiration)

    def timeout(self):
        """ return total number of seconds till
            this connection must be renewed. """
        if not self.expiration:
            return None
        remaining = remaining_time(self.expiration)
        return remaining.total_seconds() - self.grace
