import shelve
from flask import Flask, request, Response, stream_with_context
import requests


app = Flask(__name__)


BASEDIR = 'fixtures'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    with shelve.open(BASEDIR) as cache:

        if request.url not in cache:
            client_headers = {
                'Accept': request.headers['Accept']
            }
            upstream = requests.get(request.url, allow_redirects=False, headers=client_headers)

            server_headers = {
                'Content-Type': upstream.headers['content-type'],
                'Location': upstream.headers['location']
            }
            response = Response(response=upstream.content, status=upstream.status_code, headers=server_headers)
            cache[request.url] = response

        return cache[request.url]

if __name__ == "__main__":
    app.run(debug=True)
