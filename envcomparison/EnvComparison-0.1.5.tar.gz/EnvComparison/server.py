import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


def start_server():
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass = BaseHTTPServer.HTTPServer
    Protocol = "HTTP/1.0"
    port = 8000
    server_address = ('127.0.0.1', port)
    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass) 
    sa = httpd.socket.getsockname()
    print "Serving HTTP on port 8000" 
    httpd.serve_forever() 
