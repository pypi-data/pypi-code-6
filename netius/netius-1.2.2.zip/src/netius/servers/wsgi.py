#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Netius System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Netius System.
#
# Hive Netius System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Netius System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Netius System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

import netius

from netius.servers import http

SERVER_SOFTWARE = netius.IDENTIFIER
""" The server software string that is going to identify the
current service that is running on the host, the values should
include both the name and the version of it """

class WSGIServer(http.HTTPServer):
    """
    Base class for the creation of a wsgi compliant server
    the server should be initialized with the "target" app
    object as reference and a mount point.
    """

    def __init__(self, app, mount = "", decode = True, *args, **kwargs):
        http.HTTPServer.__init__(self, *args, **kwargs)
        self.app = app
        self.mount = mount
        self.mount_l = len(mount)
        self.decode = decode

    def on_connection_d(self, connection):
        http.HTTPServer.on_connection_d(self, connection)

        # verifies if there's an iterator object currently defined
        # in the connection so that it may be close in case that's
        # required, this is mandatory to avoid any memory leak
        iterator = hasattr(connection, "iterator") and connection.iterator
        if not iterator: return

        # verifies if the close attributes is defined in the iterator
        # and if that's the case calls the close method in order to
        # avoid any memory leak caused by the generator
        has_close = hasattr(iterator, "close")
        if has_close: iterator.close()

        # unsets the iterator attribute in the connection object so that
        # it may no longer be used by any chunk of logic code
        setattr(connection, "iterator", None)

    def on_data_http(self, connection, parser):
        http.HTTPServer.on_data_http(self, connection, parser)

        # method created as a clojure that handles the starting of
        # response as defined in the wsgi standards
        def start_response(status, headers):
            return self._start_response(connection, status, headers)

        # retrieves the path for the current request and then retrieves
        # the query string part for it also, after that computes the
        # path info value as the substring of the path without the mount
        path = parser.get_path()
        query = parser.get_query()
        path_info = path[self.mount_l:]

        # verifies if the path and query values should be encoded and if
        # that's the case the decoding process should unquote the received
        # path and then convert it into a valid string representation, this
        # is especially relevant for the python 3 infra-structure, this is
        # a tricky process but is required for the wsgi compliance
        if self.decode: path_info = self._decode(path_info)

        # retrieves a possible forwarded protocol value from the request
        # headers and calculates the appropriate (final scheme value)
        # taking the proxy value into account
        forwarded_protocol = parser.headers.get("x-forwarded-proto", None)
        scheme = "https" if connection.ssl else "http"
        scheme = forwarded_protocol if forwarded_protocol else scheme

        # initializes the environment map (structure) with all the cgi based
        # variables that should enable the application to handle the request
        # and respond to it in accordance
        environ = dict(
            REQUEST_METHOD = parser.method.upper(),
            SCRIPT_NAME = self.mount,
            PATH_INFO = path_info,
            QUERY_STRING = query,
            CONTENT_TYPE = parser.headers.get("content-type", ""),
            CONTENT_LENGTH = "" if parser.content_l == -1 else parser.content_l,
            SERVER_NAME = self.host,
            SERVER_PORT = str(self.port),
            SERVER_PROTOCOL = parser.version_s,
            SERVER_SOFTWARE = SERVER_SOFTWARE,
            REMOTE_ADDR = connection.address[0]
        )

        # updates the environment map with all the structures referring
        # to the wsgi specifications note that the message is retrieved
        # as a buffer to be able to handle the file specific operations
        environ["wsgi.version"] = (1, 0)
        environ["wsgi.url_scheme"] = scheme
        environ["wsgi.input"] = parser.get_message_b()
        environ["wsgi.errors"] = sys.stderr
        environ["wsgi.multithread"] = False
        environ["wsgi.multiprocess"] = False
        environ["wsgi.run_once"] = False
        environ["wsgi.server_name"] = netius.NAME
        environ["wsgi.server_version"] = netius.VERSION

        # iterates over all the header values that have been received
        # to set them in the environment map to be used by the wsgi
        # infra-structure, not that their name is capitalized as defined
        # in the standard specification
        for key, value in parser.headers.items():
            key = "HTTP_" + key.replace("-", "_").upper()
            environ[key] = value

        # runs the app logic with the provided environment map and starts
        # response clojure and then iterates over the complete set of values
        # in the returned iterator to send the messages to the other end
        # note that the iterator is set in the connection for latter retrieval
        sequence = self.app(environ, start_response)
        iterator = iter(sequence)
        connection.iterator = iterator

        # triggers the start of the connection iterator flushing operation
        # by calling the send part method for the current connection, this
        # should start reading data from the iterator and sending it to the
        # connection associated (recursive approach)
        self._send_part(connection)

    def _start_response(self, connection, status, headers):
        # retrieves the parser object from the connection and uses
        # it to retrieve the string version of the http version
        parser = connection.parser
        version_s = parser.version_s

        # adds an extra space to the status line and then
        # splits it into the status message and the code
        status_c, _status_m = (status + " ").split(" ", 1)
        status_c = int(status_c)

        # converts the provided list of header tuples into a key
        # values based map so that it may be used more easily
        headers = dict(headers)

        # tries to retrieve the content length value from the headers
        # in case they exist and if the value of them is zero the plain
        # encoding is set in order to avoid extra problems while using
        # chunked encoding with zero length based messages
        length = headers.get("Content-Length", -1)
        length = 0 if status_c in (204, 304,) else length
        if length == 0: connection.set_encoding(http.PLAIN_ENCODING)

        # verifies if the current connection is using a chunked based
        # stream as this will affect some of the decisions that are
        # going to be taken as part of response header creation
        is_chunked = connection.is_chunked()

        # checks if the provided headers map contains the definition
        # of the content length in case it does not unsets the keep
        # alive setting in the parser because the keep alive setting
        # requires the content length to be defined or the target
        # encoding type to be chunked
        has_length = not length == -1
        if not has_length: parser.keep_alive = is_chunked

        # applies the base (static) headers to the headers map and then
        # applies the parser based values to the headers map, these
        # values should be dynamic and based in the current state
        # finally applies the connection related headers to the current
        # map of headers so that the proper values are filtered and added
        self._apply_base(headers)
        self._apply_parser(parser, headers)
        self._apply_connection(connection, headers)

        # creates the list that will hold the various header string and
        # that is going to be used as buffer and then generates the various
        # lines for the headers and sets them in the buffer list
        buffer = []
        buffer.append("%s %s\r\n" % (version_s, status))
        for key, value in headers.items():
            buffer.append("%s: %s\r\n" % (key, value))
        buffer.append("\r\n")

        # joins the header strings list as the data string that contains
        # the headers and then sends the value through the connection
        data = "".join(buffer)
        connection.send_plain(data)

    def _send_part(self, connection):
        # unsets the is final flag and invalidates the data object to the
        # original unset value, these are the default values
        is_final = False
        data = None

        # extracts both the parser and the iterator from the connection
        # object so that they may be used for the current set of operations
        parser = connection.parser
        iterator = connection.iterator

        # tries to retrieve data from the current iterator and in
        # case the stop iteration is received sets the is final flag
        # so that no more data is sent through the connection
        try: data = next(iterator)
        except StopIteration: is_final = True

        # in case the connection is not meant to be kept alive must
        # must set the callback of the flush operation to the close
        # function so that the connection is closed, this callback
        # method is only going to be used if this is the final iteration
        if parser.keep_alive: callback = None
        else: callback = self._close

        # in case the final flag is set runs the flush operation in the
        # connection setting the proper callback method for it so that
        # the connection state is defined in the proper way (closed or
        # kept untouched) otherwise sends the retrieved data setting the
        # callback to the current method so that more that is sent
        if is_final: connection.flush(callback = callback)
        else: connection.send(data, delay = True, callback = self._send_part)

    def _close(self, connection):
        connection.close(flush = True)

    def _decode(self, value):
        """
        Decodes the provided quoted value, normalizing it according
        to both the pep 333 and the pep 333.

        Note that python 3 enforces the encapsulation of the string
        value around a latin 1 encoded unicode string.

        @type value: String
        @param value: The quoted value that should be normalized and
        decoded according to the wsgi 1.0/1.0.1 specifications.
        @rtype: String
        @return: The normalized version of the provided quoted value
        that is ready to be provided as part of the environ map.
        @see: http://python.org/dev/peps/pep-3333
        """

        value = netius.unquote(value)
        is_unicode = netius.is_unicode(value)
        value = value.encode("utf-8") if is_unicode else value
        value = netius.str(value)
        return value

if __name__ == "__main__":
    import logging

    def app(environ, start_response):
        status = "200 OK"
        contents = "Hello World"
        content_l = len(contents)
        headers = (
            ("Content-Length", content_l),
            ("Content-type", "text/plain"),
            ("Connection", "keep-alive")
        )
        start_response(status, headers)
        yield contents

    server = WSGIServer(app = app, level = logging.INFO)
    server.serve(env = True)
