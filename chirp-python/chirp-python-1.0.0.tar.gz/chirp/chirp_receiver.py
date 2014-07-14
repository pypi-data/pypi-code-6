import threading,socket,struct,time,json
from chirp import ChirpDecoder
from config import MCAST_GRP,MCAST_PORT
import logging


logger = logging.getLogger(__name__)




class ChirpReceiver(threading.Thread):

    def __init__(self,_chirp_manager,_mcast_grp = MCAST_GRP,_mcast_port = MCAST_PORT):
        super(ChirpReceiver,self).__init__()
        self._stopping = False
        self._pause = 5
        self.mcast_grp = _mcast_grp
        self.mcast_port = _mcast_port
        self.chirp_manager = _chirp_manager

    def run(self):
        logger.debug("chirp listener about to listen to chirps")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.mcast_grp, self.mcast_port))
        mreq = struct.pack("4sl", socket.inet_aton(self.mcast_grp), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while not self._stopping:
            msg = sock.recv(10240)
            try:
                chirp = json.loads(msg,cls=ChirpDecoder)
                self.chirp_manager.notify(chirp)
            except Exception as e:
                logger.error("message could not be interpreted", exc_info=True)
            time.sleep(self._pause)


    def stop(self):
        self._stopping = True

