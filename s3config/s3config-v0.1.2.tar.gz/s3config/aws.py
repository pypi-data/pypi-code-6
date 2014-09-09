#!/usr/bin/env python
#
# S3Config
# Copyright (c) 2014, Giacomo Marinangeli <jibbolo@gmail.com>
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library.

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket

class S3KeyError(Exception):pass

def fetch_file(bucket_name,key_name,aws_access=None,aws_secret=None):
    connection = S3Connection(aws_access,aws_secret)
    bucket = connection.get_bucket(bucket_name)
    key = bucket.get_key(key_name)
    if key is None: 
        raise S3KeyError("Invalid key_name {0}".format(key_name))
    return key.get_contents_as_string()
