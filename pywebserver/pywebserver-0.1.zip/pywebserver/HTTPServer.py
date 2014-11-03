#!/usr/bin/python3

import socket
import os
import argparse
from os.path import isdir


class HTTPServer():

    BUFFER_SIZE = 1024*8

    def __init__(self, port=80, verbose=False):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", args.port))
        sock.listen(1)
        self.sock = sock
        self.conn = None
        self.addr = None
        self.verbose = verbose
        self.cwd = os.getcwd()
        self.serve_path = os.path.dirname(os.path.realpath(__file__))
        if self.verbose:
            print("ready")

    def run(self):
        try:
            while True:
                conn, addr = self.sock.accept()
                self.conn = conn
                self.addr = addr

                if self.verbose:
                    print("\nconnection: " + addr[0])

                data = conn.recv(HTTPServer.BUFFER_SIZE)
                if not data:
                    conn.close()
                    continue

                request = HTTPRequest(data)

                if request.error_code is not None:
                    self.handle_error(request.errno, request.errstr)
                else:
                    if self.verbose:
                        print(request.path)
                    self.handle_request(request)

                conn.close()
        except KeyboardInterrupt:
            if self.verbose:
                print("\nCaught keyboard interrupt. Shutting down.")

            if self.conn is not None:
                self.conn.close()
            self.sock.close()

    def handle_request(self, request):
        request.file = None
        if isdir(self.cwd + request.path):
            try:
                path = self.cwd + request.path + "/index.html"
                request.file = open(path, "rb")
                request.fileSize = os.stat(path).st_size
            except IOError as e:
                if request.verbose:
                    print(str(e.errno) + " " + e.errstr)
                try:
                    path = self.cwd + request.path + "/index.htm"
                    request.file = open(path, "rb")
                    request.fileSize = os.stat(path).st_size
                except IOError as f:
                    if request.verbose:
                        print(str(f.errno) + " " + f.errstr)
                    # should generate index here but 404 for now
                    self.handle_error(404, "File not found.")
            if request.file is not None:
                header = self.generate_response_header(
                    200, "OK", "text/html", request.fileSize)
                self.conn.send(bytes(header, "utf-8"))
                self.conn.send(request.file.read())

            else:
                try:
                    path = self.cwd + request.path
                    request.file = open(path, "rb")
                    request.fileSize = os.stat(path).st_size
                    header = self.generate_response_header(
                        200, "OK", "text/html", request.fileSize)
                    self.conn.send(bytes(header, "utf-8"))
                    self.conn.send(request.file.read())
                except IOError as e:
                    if request.verbose:
                        print(str(f.errno) + " " + f.errstr)
                    self.handle_error(404, "File not found.")

    def handle_error(self, errno, errstr):
        fd = errstr
        size = len(fd)
        try:
            path = self.serve_path + "/errors/" + str(errno) + ".html"
            fd = open(path, "rb")
            size = os.stat(path).st_size
        except IOError:
            print("Error opening error")
            path = self.serve_path + "/errors/500.html"
            fd = open(path, "rb")
            size = os.stat(path).st_size

        header = self.generate_response_header(
            errno, errstr, "text/html", size)
        self.conn.send(bytes(header, "utf-8"))
        self.conn.send(fd.read())

    def generate_response_header(self, code, message, type, length):
        header = "HTTP/1.1 " + str(code) + " " + message + "\r\n"
        header += "Content-Type: " + type + "; charset=utf-8\r\n"
        header += "Content-Length: " + str(length) + "\r\n\r\n"
        return header


class HTTPRequest:
    def __init__(self, request, verbose=False):
        self.verbose = verbose
        self.fullRequest = str(request, "utf-8")
        self.error_code = self.error_message = None
        self.parse_request()

    def parse_request(self):
        requestline = self.fullRequest.split("\r\n")[0]
        self.path = requestline.split()[1]

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, nargs="?", default=8888,
        help="The port to run on. Defaults to 8888."
    )
    parser.add_argument("-v", "--verbose", action="store_true",
        help="Verbosity."
    )
    args = parser.parse_args()

    server = HTTPServer(port=args.port, verbose=args.verbose)
    server.run()
