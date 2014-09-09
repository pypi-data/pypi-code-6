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

import re, os
from .parser import Parser
from .aws import fetch_file

class S3Config(object):
    
    re_s3_url = re.compile('^s3://([^/]+)/(.+)$')
    
    def __init__(self, url_s3, schema=None, aws_access=None, aws_secret=None, silent_fail=False):
        self.url_s3 = url_s3
        self.aws_access = aws_access
        self.aws_secret = aws_secret
        self.parser = Parser()
        self.bucket, self.key = self.parse_url()
        self.silent_fail = silent_fail
        if schema is None:
            self.schema = self.schema_from_key(self.key)
        else:
            self.schema = schema
    
    @staticmethod
    def schema_from_key(key):
        try:
            return os.path.splitext(key)[1].replace(".","")
        except IndexError:
            return ""
            
    def fetch(self):
        return fetch_file(self.bucket,self.key,self.aws_access,self.aws_secret)
        
    def parse_data(self,data):
        parser = Parser(self.schema)
        return parser.parse(data)
        
    def parse_url(self):
        try:
            return self.re_s3_url.findall(self.url_s3)[0]
        except IndexError:
            raise ValueError("Invalid URL {0}".format(self.url_s3))
        
    def read(self):
        try:
            data = self.fetch()
            return self.parse_data(data)
        except Exception:
            if not self.silent_fail: 
                raise
            else: 
                return None