"""Interaction with the balancer manager. Only pure HTTP without knowing
anything about the domain.
"""

import re
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

    def send_form(self, form):
        """Sends a form to the balancer manager.

        :param form: A dictionary with the form parameters.
        """
        form_to_send = convert_values_to_string(form)
        form_to_send['nonce'] = self.__get_nonce_for_cluster(form['b'])
        requests.post(self._url, data=form_to_send)

    def __get_nonce_for_cluster(self, cluster):
        """Returns the nonce for the specified cluster."""
        page = self.get_balancer_manager_page()
        pattern = r'b=' + re.escape(cluster) + r'&nonce=([a-f0-9\-]+)'
        return re.findall(pattern, page)[0]

def convert_values_to_string(form):
    """Creates a new dictionary that has all non-string values replaced
    by strings that can be handled by the balancer manager.

    :param form: A dictionary.
    """
    new_form = dict()
    for key, value in form.items():
        new_form[key] = to_string(value)
    return new_form

def to_string(value):
    """Returns a string for the value that can be handled by the
    balancer manager.

    :param value: Any value.
    """
    if isinstance(value, bool):
        return '1' if value else '0'
    elif value:
        return str(value)
    else:
        return ''
