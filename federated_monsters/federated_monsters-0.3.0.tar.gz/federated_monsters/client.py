# -*- coding: utf-8 -*-
"""This contains the Box class, which is used to run a server."""
import socket
import uuid
import json
try:
    from global_vars import *
except ImportError:
    from federated_monsters.global_vars import *
try:
    from monster import Monster, Move
except ImportError:
    from federated_monsters.monster import Monster, Move

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('localhost', 8888))
# conn.send("/echo hello world".encode(ENC_))
m = Monster("Smoke", uuid.uuid1().hex, "normal",
            [Move("Scratch", "normal", "attack", 5)])
exp = m.export_monster()
j = json.dumps(exp)
send_msg = "/uploadmonster %s" % j
conn.send(send_msg.encode(ENC_))

while True:
    data = conn.recv(PACK_SIZE_)
    if not data:
        break

    print(data.decode(ENC_))
