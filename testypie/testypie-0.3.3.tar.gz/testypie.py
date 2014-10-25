import json
import os
from flask import Flask, request, Response
import requests
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
from httplib2 import iri2uri


app = Flask(__name__)


BASEDIR = 'fixtures'


def url_to_filename(url):
    return quote(iri2uri(url), safe='')


class Cache(object):
    def __init__(self, basedir):
        self.basedir = basedir

    def __contains__(self, item):
        filename = os.path.join(self.basedir, url_to_filename(item))
        return os.path.exists(filename)

    def __setitem__(self, key, value):
        filename = os.path.join(self.basedir, url_to_filename(key))

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, 'w') as cache_file:
            cache_file.write(json.dumps(value, indent=4))

    def __getitem__(self, item):
        filename = os.path.join(self.basedir, url_to_filename(item))

        with open(filename, 'r') as cache_file:
            value = json.loads(cache_file.read())
        return value


def create_incoming_headers(upstream_response):
    server_headers = {}
    for wanted_header in {'Content-Type', 'Location'}:
        if wanted_header in upstream_response.headers:
            server_headers[wanted_header] = upstream_response.headers[wanted_header]
    return server_headers


def create_outgoing_headers():
    client_headers = {
        'Accept': request.headers['Accept']
    }
    return client_headers


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):

    cache = Cache(BASEDIR)

    if request.url not in cache:

        # Use requests to fetch the upstream URL the client wants
        outgoing_headers = create_outgoing_headers()
        upstream = requests.get(request.url, allow_redirects=False, headers=outgoing_headers)

        response_headers = create_incoming_headers(upstream)
        response = dict(code=upstream.status_code, body=upstream.content.decode('utf-8'), headers=response_headers)

        cache[request.url] = response

    response = cache[request.url]
    return Response(response=response['body'].encode('utf-8'), status=response['code'], headers=response['headers'])



if __name__ == "__main__":
    app.run()
