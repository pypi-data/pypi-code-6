import logging
import json
import requests


class SlackHandler(logging.Handler):  # Inherit from logging.Handler

    def __init__(self, domain, token, channel, name='LOGGER'):
        logging.Handler.__init__(self)
        self.domain = domain
        self.token = token
        self._url = "https://%s/services/hooks/incoming-webhook?token=%s" % \
            (self.domain, self.token)
        self.channel = channel
        self.name = name

    def emit(self, record):
        payload = {
            'channel': self.channel,
            'username': self.name,
            'text': record.message
        }
        r = requests.post(
            self._url,
            headers={
                'content-type': 'application/json'
            },
            data=json.dumps(payload)
        )
