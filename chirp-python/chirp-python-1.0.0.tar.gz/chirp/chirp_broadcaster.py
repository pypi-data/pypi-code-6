import socket
import json
import threading
from chirp import Chirp,ChirpEncoder
from config import _PUBlISH,_STOP,_DISCOVER,MCAST_GRP,MCAST_PORT
import logging

logger = logging.getLogger(__name__)


class ChirpBroadcaster():

    def __init__(self,_chirp_manager,_mcast_grp = MCAST_GRP,_mcast_port = MCAST_PORT):
        self.mcast_grp = _mcast_grp
        self.mcast_port = _mcast_port
        self.chirp_manager  = _chirp_manager

    def broadcast(self,msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(msg, (self.mcast_grp, self.mcast_port))

    def broadcast_chirp(self,chirp):
        message = json.dumps(chirp, cls = ChirpEncoder)
        self.broadcast(message)

    def publish(self):
        chirp = Chirp(_PUBlISH,
                        self.chirp_manager.name,
                        self.chirp_manager.uri,
                        self.chirp_manager.port,
                        self.chirp_manager.protocol)
        self.broadcast_chirp(chirp)

    def shutdown(self):
        chirp = Chirp(_STOP,self.chirp_manager.name)
        self.broadcast_chirp(chirp)

    def discover(self,name = ''):
        chirp = Chirp(_DISCOVER,name,_sender= self.chirp_manager.name)
        logger.debug(str(threading.current_thread().ident) + ' broadcasting --  '+ json.dumps(chirp, cls = ChirpEncoder))
        self.broadcast_chirp(chirp)


