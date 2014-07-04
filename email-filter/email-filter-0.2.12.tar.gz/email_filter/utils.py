# -*- coding: utf-8 -*-
from email_filter.models import is_project_recipient


def is_outgoing(msg):
    recipients = [msg['To']]
    if recipients and ',' in recipients[0]:
        recipients = recipients[0].split(',')
    for recipient in recipients:
        if is_project_recipient(recipient.strip()):
            return False
    return True


def get_attachments(msg):
    """
    Return list of (filename, file_obj) tuples for attachments of msg.

    excepts ``msg`` to be instance of ``email.message.Message``

    """
    attaches = []
    for part in msg.walk():
        if part.get("Content-Disposition"):
            filename = part.get_filename()
            data = part.get_payload(decode=True)
            content_type = part.get_content_type()
            attaches.append((filename, data, content_type))
    return attaches
