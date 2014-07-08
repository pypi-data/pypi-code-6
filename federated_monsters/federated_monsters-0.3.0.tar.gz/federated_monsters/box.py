# -*- coding: utf-8 -*-
"""This contains the Box class, which is used to run a server."""

import socket
# import sys
import threading
import re
import json
try:
    from berkeley_db import BerkeleyDB as DB
except ImportError:
    from federated_monsters.berkeley_db import BerkeleyDB as DB
try:
    from db import DBException
except ImportError:
    from federated_monsters.db import DBException
try:
    from global_vars import *
except ImportError:
    from federated_monsters.global_vars import *


class Box(object):

    """A class to contain represent a storage server instance.

    Attributes:
        host (str): The host to be used. Left blank since it's a local server.
        port (int): The port to run the server on.
        response_needed (bool): Whether the server needs an input from the
            client to continue.
        last_req (tuple of str): The tuple of the command and the arguments
            that required a client response.
        repeat_attempts (int): The number of times the server has attempted to
            fulfill a client request.
        db (object): An instance of a DB class.
    """

    def __init__(self, port=8888):
        """Init Box with port.

        Args:
            port (int, optional): The port on which the server will be run.
        """
        self.host = ''   # Symbolic name meaning all available interfaces
        self.port = port  # Arbitrary non-privileged port
        self.response_needed = False
        self.last_req = ()
        self.repeat_attempts = 0
        self.db = DB()

    def client_thread(self, conn):
        """Handle connections to the server. Used to spawn threads.

        Args:
            conn (socket.socket): A socket object to connect to.

        Returns:
            None
        """
        # Sending message to connected client
        self.print_stream(conn, "100 CONNECTED Hello, and welcome to %s\n"
                          % socket.gethostbyname(socket.gethostname()))

        # Infinite loop so that function do not terminate and thread do not end
        while True:
            # Receiving from client
            data = conn.recv(PACK_SIZE_)
            if not data:
                break

            self.respond_to_input(conn, data.decode(ENC_))

        # Come out of loop
        conn.close()

    def respond_to_input(self, conn, text):
        """Parse and respond to data sent to the server.

        Args:
            conn (socket.socket): The socket to which the string is sent.
            text (str): The text to be parsed by the server.

        Returns:
            bool: True if successful, False if error.
        """
        words = text.strip().split(" ")
        cmd = words[0].lower()
        args = words[1:]

        if not self.response_needed:
            if cmd == "/echo":
                return self.print_stream(conn, "200 OK %s" % " ".join(args))
            elif cmd == "/uploadmonster":
                j = " ".join(args)
                val = json.loads(j)
                print(self.check_hash(val[0]))
                r = self.db.add_entry(val[0].lower(), val[1])
                return self.print_stream(conn, "200 OK" if r else "500 FAIL")
            elif cmd == "/downloadmonster":
                j = " ".join(args)
                print(self.check_hash(j))
                try:
                    r = self.db.get_entry(j.lower())
                    print(j, r)
                    self.last_req = (cmd, j)
                    self.response_needed = True
                    return self.print_stream(conn,
                                             "101 RESPONOSE_REQUIRED %s" % r)
                except DBException:
                    return self.print_stream(conn, "500 FAIL")
            else:
                return self.print_stream(conn, "403 BAD_COMMAND %s" % cmd)
        else:
            if self.last_req[0] == "/downloadmonster":
                if cmd == "200":
                    self.repeat_attempts = 0
                    self.last_req = ()
                    self.response_needed = False
                    return self.print_stream(conn, "200 OK")
                else:
                    self.repeat_attempts += 1
                    self.respond_to_input(conn, " ".join(self.last_req))

    def print_stream(self, conn, text):
        """Send text to a socket connection.

        Args:
            conn (socket.socket): The socket to which the string is sent.
            text (str): The text to send.

        Returns:
            bool: True if successful, False if error.
        """
        try:
            conn.sendall(text.encode(ENC_))
            return True
        except socket.error:
            return False

    def check_hash(self, hash_digest):
        """Check whether a string is a valid SHA512 hash.

        Args:
            hash_digest (str): The hex digest of the hash to check.

        Returns:
            bool: True if the hash is valid, False otherwise.
        """
        hashes = re.findall(r"([a-fA-F\d]{128})", hash_digest)
        return bool(len(hashes))

    def run(self):
        """Execute the main loop of the server.

        Returns:
            bool: True if successful, False if socket error.
        """
        self.db.open_db()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        # Bind socket to local host and port
        try:
            sock.bind((self.host, self.port))
        except socket.error as msg:
            print('Bind failed. Error Code: '+str(msg[0])+' Message '+msg[1])
            return False

        print('Socket bind complete')

        # Start listening on socket
        sock.listen(10)
        print('Socket now listening')

        # Keep talking with the client
        while True:
            # Wait to accept a connection - blocking call
            conn, addr = sock.accept()
            print('Connected with ' + addr[0] + ':' + str(addr[1]))

            # Start a new thread
            thr = threading.Thread(target=self.client_thread, args=(conn,))
            thr.start()

        self.db.close()
        sock.close()
        return True
