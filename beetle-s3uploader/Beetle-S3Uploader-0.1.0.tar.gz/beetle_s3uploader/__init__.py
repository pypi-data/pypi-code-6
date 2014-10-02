from boto.s3.connection import S3Connection, Key
from boto.exception import S3ResponseError
import mimetypes
import zlib
import os


class Uploader:
    def __init__(self, gzip, headers, writer, bucket_name):
        self.writer = writer
        self.bucket_name = bucket_name
        self.gzip = gzip
        self.headers = [h.split(':') for h in headers]

        # Using environment variables or ~/.boto
        self.connection = S3Connection()
        self.bucket = self.get_bucket()

    def get_bucket(self):
        try:
            return self.connection.get_bucket(self.bucket_name)
        except S3ResponseError as err:
            return self.connection.create_bucket(self.bucket_name)

    def get_files(self):
        for destination, content in self.writer.files():
            content_type, content_encoding = mimetypes.guess_type(destination)
            prefix, suffix = content_type.split('/')
            gzipped = False
            if self.gzip and prefix not in {'image'}:
                compressor = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
                content = compressor.compress(content) + compressor.flush()
                gzipped = True
            yield destination, content, content_type, gzipped

    def upload(self):
        for destination, data, content_type, compressed in self.get_files():
            key = Key(self.bucket)
            key.content_type = content_type
            if compressed:
                key.set_metadata('content-encoding', 'gzip')

            for header, value in self.headers:
                key.set_metadata(header, value)
            key.key = destination
            key.set_contents_from_string(data)

    def clean(self):
        for key in self.bucket.get_all_keys():
            key.delete()


def register(ctx, config):
    gzip = config.get('gzip', False)
    headers = config.get('headers', [])

    uploader = Uploader(gzip, headers, ctx.writer, ctx.config.site['domain'])
    ctx.commander.add('s3upload', uploader.upload, 'Upload the rendered site')
    ctx.commander.add('s3clean', uploader.clean, 'Delete everything in the S3 bucket')
