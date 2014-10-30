"""Quaidan is a python wrapper for mod_proxy_balancer's balancer
manager. The starting point for all interactions is a
``BalancerManager`` object. This object provides the status and
can be used to update members.
"""

__version__ = '0.2.1'

from quaidan.client import Client
from quaidan.status import parse_balancer_manager_page

class BalancerManager(object):
    """The starting point for all interactions with the balancer
    manager page.
    """

    def __init__(self, url):
        self._client = Client(url)

    def get_status(self):
        """Returns the current status of the balancer.

        :returns: an Status object with the current status of the
            balancer.
        """
        page = self._client.get_balancer_manager_page()
        return parse_balancer_manager_page(page)

    def send_command(self, command):
        """Sends a command to the balancer.

        :param command: the command that is send to the balancer.
        """
        self._client.send_form(command.to_form())
