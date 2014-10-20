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
            print("Nothing stored for {}; fetching...".format(request.url))
            client_headers = {
                'Accept': request.headers['Accept']
            }
            upstream = requests.get(request.url, allow_redirects=False, headers=client_headers)

            server_headers = {}
            for wanted_header in {'Content-Type', 'Location'}:
                if wanted_header in upstream.headers:
                    server_headers[wanted_header] = upstream.headers[wanted_header]

            response = Response(response=upstream.content, status=upstream.status_code, headers=server_headers)
            cache[request.url] = response

        return cache[request.url]

if __name__ == "__main__":
    app.run(debug=True)
