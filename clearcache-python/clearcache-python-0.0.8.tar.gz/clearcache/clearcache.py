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

    def __init__(self, hostnames, varnish_nodes):
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

        if isinstance(hostnames, list) and hostnames:
            for hostname in hostnames:
                if not is_valid_hostname(hostname):
                    raise HostnameException('Hostname is not valid: ' + hostname)
            self.hostnames = hostnames
        else:
            self.hostnames = None
            HostnameException('No hostnames were provided')


    def ban_url_list(self, url_list):
        """
        Bans a list of urls.
        """
        if isinstance(url_list, list) and url_list:
            if self.hostnames and self.varnish_nodes:
                url_combo = '(' + '|'.join(url_list) + ')'

                for hostname in self.hostnames:
                    header = {'X-Ban-Url': url_combo, 'X-Ban-Host': hostname}

                    s = Session()
                    for node in self.varnish_nodes:
                        try:
                            req = Request('BAN', node,
                                headers=header
                            )
                            prepped = req.prepare()

                            resp = s.send(prepped,
                                          timeout=2)
                        except Exception:
                            log.error('Error sending ban to ' + node)
                        else:
                            if codes.ok != resp.status_code:
                                log.error('Error sending ban to ' + node)
            else:
                log.warning('No varnish nodes provided to clear the cache')
        else:
            log.warning('No URLs provided')
