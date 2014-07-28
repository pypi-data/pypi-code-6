"""
"""
__version__ = '0.1.0'

__all__ = [
    'RIPMiddleware'
]

import logging

import netaddr


logger = logging.getLogger(__name__)


class RIPMiddleware(object):
    """
    Sets REMOTE_ADDR from X-Forwarded-For, accounting for proxies.
    """

    def __init__(self, next_app, internal=None, proxies=None):
        """
        :param internal:
            CIDR string defining the internal network (e.g. 192.0.2.0/24).If
            more than one define a list of such CIDR strings. Defaults to
            '10.0.0.0/8'. These can be thought of as *internal* proxies.

        :param proxies:
            Optional dictionary mapping a proxy IP to its internal network
            CIDR:

                {
                '50.18.213.180': '10.0.0.0/8'
                }

            Defaults to {}. These can be thought of as *external* proxies.

        """
        self.next_app = next_app
        internal = internal or ['10.0.0.0/8']
        if not isinstance(internal, (list, tuple)):
            internal = [internal]
        self.internals = map(netaddr.IPNetwork, internal)
        self.proxies = []
        for proxy_addr, proxy_internals in (proxies or {}).iteritems():
            proxy_addr = netaddr.IPNetwork(proxy_addr)
            if not isinstance(proxy_internals, (list, tuple)):
                proxy_internals = [proxy_internals]
            proxy_internals = map(netaddr.IPNetwork, proxy_internals)
            self.proxies.append((proxy_addr, proxy_internals))

    def _proxy(self, addr):
        for proxy, internals in self.proxies:
            if addr in proxy:
                return internals
        return None

    def __call__(self, environ, start_response):
        internals = self.internals
        if 'HTTP_X_FORWARDED_FOR' in environ:
            addr = environ['REMOTE_ADDR']
            for raw in reversed(environ['HTTP_X_FORWARDED_FOR'].split(',')):
                try:
                    addr = netaddr.IPAddress(raw.strip())
                except netaddr.AddrFormatError:
                    logger.info(
                        'invalid IP address "%s" in X-Forwarded-For header '
                        '"%s"', addr, environ['HTTP_X_FORWARDED_FOR']
                    )
                    break
                if any(addr in network for network in internals):
                    continue
                internals = self._proxy(addr)
                if internals:
                    continue
                break
            environ['REMOTE_ADDR'] = str(addr)
        return self.next_app(environ, start_response)
