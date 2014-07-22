#!/usr/bin/env python
import urllib2
import json
import glob
import base64
import os

class QueryCache(object):

    def __init__(self):
        self.cache_dir = ".cache"
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.cache_meta = {}
        self.read_cache()

    def read_cache(self):
        for file in glob.glob(os.path.join(self.cache_dir, '*')):
            url = base64.b64decode(os.path.split(file)[1])
            self.cache_meta[url] = {
                'location': file
            }


    def json_query(self, url):
        if url not in self.cache_meta:
            # Make web query
            self._query(url)
        return self.load_json(self.cache_meta[url])

    def load_json(self, file):
        with open(file['location'], 'rb') as cached_file:
            return json.load(cached_file)

    def _query(self, url):
        b64 = base64.b64encode(url)
        output_location = os.path.join(self.cache_dir, b64)
        with open(output_location, 'wb') as fh:
            req = urllib2.Request(url)
            f = urllib2.urlopen(req)
            fh.write(f.read())
            f.close()

            # Cache name/location of output file
            self.cache_meta[url] = {
                'location': output_location
            }


