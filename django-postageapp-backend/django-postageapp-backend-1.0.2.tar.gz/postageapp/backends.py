import json
import logging
import urllib2

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, EmailMultiAlternatives

import postageapp


logger = logging.getLogger('postageapp.backends')

if not hasattr(settings, 'POSTAGEAPP_API_KEY'):
    raise ImproperlyConfigured('Missing `POSTAGEAPP_API_KEY` setting.')

POSTAGEAPP_API_KEY = settings.POSTAGEAPP_API_KEY
POSTAGEAPP_ENDPOINT = 'https://api.postageapp.com/v.1.0/send_message.json'
POSTAGEAPP_LAYOUT_TEMPLATE = getattr(settings, 'POSTAGEAPP_LAYOUT_TEMPLATE', None)


class PostageAppEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return

        for message in email_messages:
            if not message.to:
                raise ValueError(u'Recipient is missing')

            content = {}
            if isinstance(message, EmailMessage):
                content["text/%s" % message.content_subtype] = message.body

            if isinstance(message, EmailMultiAlternatives):
                for alt in message.alternatives:
                    content[alt[1]] = alt[0]

            msgdict = {
                'api_key': POSTAGEAPP_API_KEY,
                'arguments': {
                    'recipients': message.to,
                    'headers': {
                        'subject': message.subject,
                        'from': message.from_email,
                        'bcc': message.bcc
                    },
                    'content': content
                }
            }

            if POSTAGEAPP_LAYOUT_TEMPLATE is not None:
                msgdict['template'] = POSTAGEAPP_LAYOUT_TEMPLATE

            if hasattr(message, 'extra_headers') and message.extra_headers:
                msgdict['arguments']['headers'].update(message.extra_headers)

            if hasattr(message, 'attachments') and message.attachments:
                file_string = message.attachments[0][1].encode('base64')
                attachment_dict = {
                    'attachments': {
                        'file_name': {
                            'content_type': 'application/octet-stream',
                            'content': file_string
                        }
                    }
                }
                msgdict['arguments'].update(attachment_dict)

            try:
                req = urllib2.Request(
                    POSTAGEAPP_ENDPOINT,
                    json.dumps(msgdict),
                    {'User-Agent': 'django-postageapp (%s)' % postageapp.__versionstr__,
                     'Content-Type': 'application/json'}
                )
                response = urllib2.urlopen(req)
                json_response = json.loads(response.read())

                if json_response['response']['status'] != 'ok':
                    self.error = 'Server returned %s' % json_response['response']['status']
                    logger.error(self.error)

            except urllib2.HTTPError, e:
                logger.error(e)

                if not self.fail_silently:
                    raise urllib2.HTTPError, e
