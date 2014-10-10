"""Interaction with the balancer manager. Only pure HTTP without knowing
anything about the domain.
"""

import requests

class Client(object):
    """The Client interacts with the balancer manager. It is plain
    HTML/HTTP code and doesn't know any domain object.
    """

    def __init__(self, url):
        """Creates a new client for a specfific balancer manager.

        :param url: The URL of the balancer manager
            (e.g. http://127.0.0.1/balancer-manager).
        """
        self._url = url

    def get_balancer_manager_page(self):
        """Returns the HTML of the balancer manager page."""
        response = requests.get(self._url)
        return response.text
