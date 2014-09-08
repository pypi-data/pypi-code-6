"""
The MIT License (MIT)

Copyright (c) 2013 Riccardo Cagnasso

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import requests
import json
from urllib.parse import urlparse, urlunparse, urljoin

def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/'), args))

class OpenDB(object):

    def __init__(self, address='http://opendb.netfluid.org/'):
        self.address = address

    def login(username, password):
        pass

    def get_json_response(self, path):
        url = urljoin(self.address, path)
        response = requests.get(url)
        response.encoding = 'utf-8-sig'

        return response.json()

    def post(self, path, params):
        url = urljoin(self.address, path)
        response = requests.post(url, params=params)
        response.encoding = 'utf-8-sig'

        return response.json()

    def put(self, path, params):
        url = urljoin(self.address, path)
        response = requests.put(url, params=params)
        response.encoding = 'utf-8-sig'

        return response.json()

    def request_delete(self, path):
        url = urljoin(self.address, path)
        response = requests.delete(url)
        response.encoding = 'utf-8-sig'

        return response.json()

    def collections(self):
        return self.get_json_response(urljoin('rest'))

    def items(self, collection):
        return self.get_json_response(urljoin('rest', collection))

    def item(self, collection, id):
        return self.get_json_response(urljoin('rest', collection, id))

    def add(self, collection, id, item):
        return self.post(urljoin('rest', collection, id), params=item)

    def update(self, collection, id, item):
        return self.put(urljoin('rest', collection, id), params=item)

    def delete(self, collection, id):
        return self.request_delete(urljoin('rest', collection, id))
