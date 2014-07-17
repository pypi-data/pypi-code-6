# -*- coding: utf-8 -*-
"""This contains the Box class, which is used to run a server."""

import json
import re
import socket
import threading
import datetime

# import sys
try:
    from berkeley_db import BerkeleyDB as DBClass
except ImportError:
    from federated_monsters.berkeley_db import BerkeleyDB as DBClass

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
        conn_list (list of socket.socket): A list of the socket connections
            made. To be used to send out chat messages.
        db (object): An instance of a DBClass.
    """

    def __init__(self, port=PORT_, db_fn="monsters_db"):
        """Init Box with port.

        Args:
            port (int, optional): The port on which the server will be run.
        """
        self.host = ''   # Symbolic name meaning all available interfaces
        self.port = port  # Arbitrary non-privileged port
        self.response_needed = False
        self.last_req = ()
        self.repeat_attempts = 0
        self.conn_list = []
        self.db = DBClass(db_fn)
        # self.db.open_db()

    def client_thread(self, client):
        """Handle connections to the server. Used to spawn threads.

        Args:
            conn (socket.socket): A socket object to connect to.

        Returns:
            None
        """
        # Sending message to connected client
        self.print_stream(client, "100 CONNECTED Hello, and welcome to %s\n"
                          % socket.gethostbyname(socket.gethostname()))

        # Infinite loop so that function do not terminate and thread do not end
        while True:
            # Receiving from client
            data = client.conn.recv(PACK_SIZE_)
            if not data:
                print("Disconnected")
                self.conn_list = [x for x in self.conn_list if x != client]
                break

            self.respond_to_input(client, data.decode(ENC_))

        # Come out of loop
        client.conn.close()

    def respond_to_input(self, client, text):
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
        print(text)

        if not self.response_needed:
            if cmd == "/echo":
                return self.print_stream(client, "200 OK %s" % " ".join(args))
            elif cmd == "/uploadmonster":
                j = " ".join(args)
                val = json.loads(j)
                # print(text)
                # print(self.check_hash(val[0]))
                # print("val", " ".join(val[1:]))
                r = self.db.add_entry(val[0].lower(), " ".join(val[1:]))
                # print(r)
                return self.print_stream(client, "200 OK" if r else "500 FAIL")
            elif cmd == "/downloadmonster":
                j = " ".join(args)
                print(self.check_hash(j))
                try:
                    r = self.db.get_entry(j.lower())
                    print(j, r)
                    self.last_req = (cmd, j)
                    self.response_needed = True
                    return self.print_stream(client,
                                             "101 RESPONOSE_REQUIRED %s" % r)
                except DBException:
                    return self.print_stream(client, "500 FAIL")
            elif cmd == "/chat":
                j = " ".join(args)
                self.chat_msg(client.conn.getpeername()[0], j)
            elif cmd == "/chatoff":
                client.chat = False
            elif cmd == "/chaton":
                client.chat = True
            else:
                return self.print_stream(client, "403 BAD_COMMAND %s" % cmd)
        else:
            if self.last_req[0] == "/downloadmonster":
                if cmd == "200":
                    self.repeat_attempts = 0
                    self.last_req = ()
                    self.response_needed = False
                    return self.print_stream(client, "200 OK")
                else:
                    self.repeat_attempts += 1
                    self.respond_to_input(client, " ".join(self.last_req))

    def chat_msg(self, from_ip, text):
        """Send a chat message to all connected clients.

        Args:
            from_ip (str): The IP of the client sending the message.
            text (str): The text of the message.
        """
        t = datetime.datetime.now().time().strftime("%H:%M:%S")
        for i in self.conn_list:
            if i.chat:
                self.print_stream(i, "300 CHAT_MSG [%s %s]: %s"
                                  % (from_ip, t, text))
            else:
                print("Chat off")

    def print_stream(self, client, text):
        """Send text to a socket connection.

        Args:
            conn (socket.socket): The socket to which the string is sent.
            text (str): The text to send.

        Returns:
            bool: True if successful, False if error.
        """
        text = text+"\n"
        try:
            client.conn.sendall(text.encode(ENC_))
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

    def check_uuid(self, uuid_hex):
        """Check whether a string is a valid :rfc:`4122` UUID.

        Args:
            uuid_hex (str): The hex representation of the UUID.

        Returns:
            bool: True if it is a valid UUID, False otherwise.
        """
        try:
            uuid.UUID(uuid_hex)
            return True
        except ValueError:
            return False

    def run(self):
        """Execute the main loop of the server.

        Returns:
            bool: True if successful, False if socket error.
        """
        self.db.open_db()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)

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
        try:
            while True:
                print(self.conn_list)
                # Wait to accept a connection - blocking call
                # try:
                conn, addr = sock.accept()
                # except KeyboardInterrupt:
                #     for i in self.conn_list:
                #        i.close()
                #    break
                print('Connected with ' + addr[0] + ':' + str(addr[1]))

                # conn.chat = True
                # setattr(conn, "chat", True)
                client = Client(conn)

                self.conn_list.append(client)

                # Start a new thread
                thr = threading.Thread(target=self.client_thread,
                                       args=(client,))
                thr.start()
        except KeyboardInterrupt:
            print("Quit")
            for i in self.conn_list:
                i.conn.close()

        # self.db.close()
        sock.close()
        return True


class Client(object):

    """A wrapper around socket connections to make it easier to set properties.

    In the future, it might be changed to a namedtuple.

    Attributes:
        conn (socket.socket): The client socket connection.
        chat (bool): If True, the client wishes to receive chat messages.
    """

    def __init__(self, conn, chat=True):
        """Init Client."""
        self.conn = conn
        self.chat = chat
