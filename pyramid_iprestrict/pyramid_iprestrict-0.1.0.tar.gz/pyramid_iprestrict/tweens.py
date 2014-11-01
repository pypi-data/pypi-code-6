import ipaddress

from pyramid.compat import text_type
from pyramid.httpexceptions import HTTPForbidden
from pyramid.settings import aslist


def iprestrict_tween_factory(handler, registry):
    """ Restrict access based on IP Address

    configure following parameter in config file.

    ``iprestrict.allowed_ips`` specify allowed IP Addresses. If you want to
    specify multiple IP Addresses, join them with spaces. Also, you can use
    subnets here.

    Example::

       iprestrict.allowed_ips = 127.0.0.1 192.168.0.0/24

    """
    allowed_ips = registry.settings.get('iprestrict.allowed_ips')
    if allowed_ips:
        allowed_ips = aslist(allowed_ips, True)
        allowed_ips = [ipaddress.ip_network(text_type(ip)) for ip in allowed_ips]

        def iprestrict_tween(request):
            client_addr = ipaddress.ip_address(text_type(request.client_addr))
            for allowed in allowed_ips:
                if client_addr in allowed:
                    return handler(request)
            return HTTPForbidden()

        return iprestrict_tween
    return handler
