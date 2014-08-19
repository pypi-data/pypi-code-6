import logging
import re

from requests import Request, Session, codes

log = logging.getLogger(__name__)


def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


class HostnameException(Exception):
    """
    Exception for invalid hostnames
    """
    pass


class CacheHandler:
    """
    Used to handle sending bans and purges to
    varnish nodes.
    """

    def __init__(self, hostname, varnish_nodes):
        """
        Initiate the varnish nodes to be used to
        clear the cache.
        """
        if isinstance(varnish_nodes, list) and varnish_nodes:
            varnish_nodes = ['http://' + x if not (x.startswith('http://') or x.startswith('https://')) else x for x in varnish_nodes]
            self.varnish_nodes = varnish_nodes
        else:
            self.varnish_nodes = []
            log.warning('No varnish nodes provided')

        if is_valid_hostname(hostname):
            self.hostname = hostname
        else:
            raise HostnameException('Hostname is not valid: ' + hostname)


    def ban_url_list(self, url_list):
        """
        Bans a list of urls.
        """
        if isinstance(url_list, list) and url_list:
            if self.hostname and self.varnish_nodes:
                url_combo = '(' + ''.join(url_list) + ')'

                header = {'X-Ban-Url': url_combo, 'X-Ban-Host': self.hostname}

                s = Session()
                for node in self.varnish_nodes:
                    req = Request('BAN', node,
                        headers=header
                    )
                    prepped = req.prepare()

                    resp = s.send(prepped,
                                  timeout=30)

                    if codes.ok != resp.status_code:
                        log.warning('Error sending ban to ' + node)
            else:
                log.warning('No varnish nodes provided to clear the cache')
        else:
            log.warning('No URLs provided')
