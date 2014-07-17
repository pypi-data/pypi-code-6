# -*- coding: utf-8 -*-
"""This contains functions that are helpful for running a client to a Box."""
import json
import socket
import uuid

try:
    from global_vars import *
except ImportError:
    from federated_monsters.global_vars import *

try:
    from monster import Monster, Move
except ImportError:
    from federated_monsters.monster import Monster, Move


def wait_for_response(conn, indef=False, out=False):
    """Wait for a response from the server.

    Args:
        conn (socket.socket): A socket object to connect to.
        indef (bool, optional): Whether to continue looping indefinitely.
            Defaults to False.
        out (bool, optional): Whether to print data as it is received. Defaults
            to False.

    Returns:
        str or None: The received data if it is not printed or indefinite.
    """
    while True:
        try:
            data = conn.recv(PACK_SIZE_)
        except socket.error as e:
            print(e)
            return ""
        if not data:
            break

        if out:
            print(data.decode(ENC_))

        if not out and not indef:
            return data.decode(ENC_)
        if not indef:
            break


def send_msg(conn, txt):
    """Send the given text over the given socket.

    Args:
        conn (socket.socket): A socket object to connect to.
        send_msg (str): The string to send.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        conn.send(txt.encode(ENC_))
        return True
    except socket.error as e:
        print(e)
        return False


def gen_conn(server, port=PORT_):
    """Connect to the given server on the given port.

    Args:
        server (str): An IP address or URI to which the client can connect.
        port (int, optional): The port on which the client should connect.
            Defaults to the value of
            :data:`federated_monsters.global_vars.PORT_`.

    Returns:
        socket.socket: A socket object that can be used elsewhere.

    Raises:
        socket.error: If the connection fails.
    """
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((server, port))

    return conn

if __name__ == "__main__":
    conn = gen_conn("localhost")

    wait_for_response(conn, out=True)

    m = Monster("Smoke", uuid.uuid1().hex, "normal",
                [Move("Scratch", "normal", "attack", 5)])
    exp = m.export_monster()
    j = json.dumps(exp)
    txt = "/uploadmonster %s" % j

    send_msg(conn, txt)
    print(txt)

    wait_for_response(conn, out=True, indef=True)
