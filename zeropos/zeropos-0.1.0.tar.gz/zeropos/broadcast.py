"""
Listener that announces the availability of the printing service
"""
import socket
from zeroconf import ServiceInfo, Zeroconf
from config import CONFIG


class Broadcast(object):
    """
    A zeroconf listener that broadcasts the address for the printing service
    """

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.properties = {
            'nickname': u'Printer Nickname',
            'service': u'Tryton POS'
        }
        self.service = Zeroconf()
        self._service_info = None

    @property
    def service_info(self):
        if self._service_info is None:
            self._service_info = ServiceInfo(
                "_trytonpos._tcp.local.",
                "%s._trytonpos._tcp.local." % socket.gethostname(),
                socket.inet_aton(self.address), self.port, 0, 0,
                self.properties
            )
        return self._service_info

    def register_zeroconf(self):
        """
        Register a new service for printing
        """
        print("Registration of service @ %s:%s" % (self.address, self.port))
        self.service.registerService(self.service_info)

    def unregister_zeroconf(self):
        """
        Unregister the given service
        """
        print("Unregistering...")
        self.service.unregisterService(self.service_info)
        self.service.close()


if __name__ == '__main__':
    CONFIG.parse()

    local_ip = CONFIG['address']
    port = CONFIG['port']

    broadcast = Broadcast(local_ip, port)
    try:
        broadcast.register_zeroconf()
    finally:
        broadcast.unregister_zeroconf()
