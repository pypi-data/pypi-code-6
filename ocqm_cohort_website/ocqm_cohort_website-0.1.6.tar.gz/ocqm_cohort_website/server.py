from __future__ import print_function

import sys

from . import paths

if sys.version_info >= (3, 0):
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
else:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer


def get_http_server(directory, port):
    class Daemon(TCPServer):
        allow_reuse_address = True

    Handler = SimpleHTTPRequestHandler
    return Daemon(("127.0.0.1", port), Handler)


def run_http_server(directory):
    port = 8000

    print ("serving at port", port)

    with paths.switch_path(directory):
        httpd = get_http_server(directory, port)
        httpd.serve_forever()
