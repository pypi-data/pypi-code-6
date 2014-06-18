"""Functions for coalescing part files in s3."""
from __future__ import print_function
import boto


class S3Merger():
    """A class for merging all part files in an s3 bucket"""

    def __init__(self, bucket, path):
        self.connection = boto.connect_s3()
        self.bucket = self.connection.get_bucket(bucket)
        self.parts = self.bucket.list(prefix=path)
        self._merge_parts()

    def __str__(self):
        return self.merged

    def _merge_parts(self):
        """Merge all part files into a single string and store it
        as self.merged

        """
        self.merged = ''.join([part.get_contents_as_string()
                               for part
                               in self.parts])

    def write_file(self, out_file):
        """Write self.merged to a file"""
        with open(out_file, 'w') as f:
            print(self.merged, file=f)
