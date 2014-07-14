import json
import time
import threading
import chirp_broadcaster, chirp_receiver
from chirp import ChirpEncoder
from config import _PUBlISH,_STOP,_DISCOVER,MCAST_GRP,MCAST_PORT
import logging

logger = logging.getLogger(__name__)



class ChirpManager():
    """The Chirp Manager is an interface to which allows you to
    start and publish yourself as a chirper ont he network
    discover chirpers on the network

    NOTE: [chirper / your service] is used interchangeably

    Functions:

        start_chirping():
            publish the chirper on the network and
            will initiate discovering services on the network

        list_chirpers(): will list the current chirpers available on the network

        fetch(chirper_name): fetch a chirper with the given chirper_name

        details(): will retrieve the configuration of the current chirper

        stop(): will stop the chirper and broadcast a stop message for itself


    """

    def __init__(self,_name,_port,_protocol,_uri,_config={},
                 _mcast_grp = MCAST_GRP, _mcast_port = MCAST_PORT,
                    _fetch_wait_count = 10):
        """
            NOTE: [chirper / your service] is used interchangeably

            name : name of the service/chirper
            uri : the uri for your service/chirper
            port : port at which your service is running
            protocol : protocol used by your service

            config : a dict which will be sent on each publish to all the other chirpers

            mcast_grp : the multicast group on which all chirpers would publish messages
                        default value is MCAST_GRP defined in config.py

            mcast_port : the multicast port on which all chirpers would publish messages
                        default value is MCAST_PORT defined in config.py

            fetch_wait_count : the number of times a fetch call should try discovering a
                                chirper/service on the network before returning

        """


        self.name = _name
        self.port = _port
        self.protocol = _protocol
        self.uri = _uri
        self.config = _config
        self.chirpers = {}
        self.mcast_grp = _mcast_grp
        self.mcast_port = _mcast_port
        self.fetch_wait_count = _fetch_wait_count
        self.chirp_broadcaster = chirp_broadcaster.ChirpBroadcaster(self,self.mcast_grp,self.mcast_port)
        self.chirp_receiver = chirp_receiver.ChirpReceiver(self,self.mcast_grp,self.mcast_port)
        self.chirp_receiver.setDaemon(True)

    def add_chirper(self,chirp):
        self.chirpers[chirp.name] ={'name': chirp.name,
                                    'port': chirp.port,
                                    'uri':chirp.uri,
                                    'protocol':chirp.protocol,
                                    'config':chirp.config}

    def remove_chirper(self,chirp):
        del self.chirpers[chirp.name]

    def notify(self,chirp):
        if chirp.sender != self.name:
            logger.debug(str(threading.current_thread().ident) + ' notified -- ' + json.dumps(chirp,cls=ChirpEncoder))
            if chirp.method == _PUBlISH:
                self.add_chirper(chirp)
            elif chirp.method == _STOP:
                self.remove_chirper(chirp.name)
            elif chirp.method == _DISCOVER:
                if chirp.name.strip() == '':
                    self.chirp_broadcaster.publish()
                elif chirp.name.strip() == self.name:
                    self.chirp_broadcaster.publish()
            else:
                logger.error("This bird doesn't know how to chirp")
                logger.error(json.loads(chirp,cls=ChirpEncoder))


    def details(self):
        """details() will retrieve the configuration of the current chirper"""

        return {'name': self.name,
                'port': self.port,
                'uri': self.uri,
                'protocol': self.protocol,
                'config': self.config}


    def stop(self):
        """stop() will stop the chirper and broadcast a stop message for itself"""

        self.chirp_receiver.stop();


    def list_chirpers(self):
        """list_chirpers() will list the current chirpers available on the network"""

        return self.chirpers.keys()



    def fetch(self,chirper_name):
        """fetch(chirper_name) fetch a chirper with the given chirper_name """

        if chirper_name.strip() == self.name:
            logger.debug('fetching current chirper ' + chirper_name)
            return self.details()
        elif chirper_name in self.chirpers:
            logger.debug('fetching existing chirper ' + chirper_name)
            return self.chirpers[chirper_name]
        else:
            self.chirp_broadcaster.discover(chirper_name)
            logger.debug('fetching chirper ' + chirper_name)
            count = self.fetch_wait_count
            while count < self.fetch_wait_count:
                if chirper_name in self.chirpers:
                    logger.debug('chirper found ' + chirper_name)
                    return self.chirpers[chirper_name]
                    return self.chirpers[chirper_name]
                else:
                    time.sleep(1)
                    count = count + 1
            return False

    def start_chirping(self):
        """start_chirping() will
            publish chirper on the network and
            will initiate discovering services on the network"""

        self.chirp_receiver.start()
        self.chirp_broadcaster.publish()
        self.chirp_broadcaster.discover()


