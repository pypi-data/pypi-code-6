from flask import Flask, request, Response
import os
try:
    from urllib.urlparse import quote
except ImportError:
    from urllib import quote
import requests
import json
import logging


app = Flask(__name__)


BASEDIR = 'fixtures'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    cache_file_name = os.path.join(BASEDIR, quote(request.url, ''))

    if not os.path.exists(BASEDIR):
        os.makedirs(BASEDIR)

    if not os.path.exists(cache_file_name):
        with open(cache_file_name, 'wb') as cache_file:
            logging.info('No fixture for {}; downloading...', request.url)
            upstream_response = requests.get(request.url, stream=True, allow_redirects=False)
            cache_file.write(json.dumps(dict(upstream_response.headers)))
            cache_file.write('\n')
            cache_file.write(upstream_response.raw.read())

    response = Response()

    with open(cache_file_name, 'rb') as cache_file:
        response.headers = json.loads(cache_file.readlines()[0].rstrip('\n'))

    with open(cache_file_name, 'rb') as cache_file:
        return ''.join(cache_file.readlines()[1:])

if __name__ == "__main__":
    app.run(debug=True)
