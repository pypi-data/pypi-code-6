#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import sys
import os
import email
import logging
import traceback
import cgitb
import uuid
import chardet
import pytils
cgitb.enable(format='text')

try:
    from mail_route_settings import SELF_ADDRESS, PROCESS_OUTGOING_EMAILS
except ImportError:
    SELF_ADDRESS = 'proxy@kavahq.com'
    PROCESS_OUTGOING_EMAILS = False

if __name__ == "__main__":
    try:
        from mail_route_settings import PROJECT_BASE_DIR, DJANGO_SETTINGS_MODULE, LOG_PATH
        sys.path.extend([PROJECT_BASE_DIR])
        os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
        # requires this to open SQLite database as if full path was given
        os.chdir(PROJECT_BASE_DIR)
    except ImportError:
        print("Can't import mail router settings")
        sys.exit(os.EX_CONFIG)


# This imports rely on DJANGO_SETTINGS_MODULE env variable, so do not move them to top
# thirdparty:
from annoying.functions import get_object_or_None

# Django:
from django.shortcuts import _get_queryset
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile

# Local:
from email_filter.models import (
    EmailLog, EmailRedirect, get_name_from_email,
    get_cleaned_email, is_project_recipient, is_local_email,
    EmailAttachment,
)
from email_filter.utils import is_outgoing, get_attachments
from email_filter.signals import mail_for_unknown_user

# check django settings:
from django.conf import settings

logger = logging.getLogger('mail_script')
if __name__ == "__main__":
    if not LOG_PATH:
        LOG_PATH = os.path.join(PROJECT_BASE_DIR, 'mail_route.log')
    logger.addHandler(logging.FileHandler(LOG_PATH))


def get_first_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.filter(*args, **kwargs)[0]
    except (queryset.model.DoesNotExist, IndexError):
        return None


def send_them(email_obj, msg, send_email):
    orig_from = msg['From']
    orig_to = msg['To']
    recipient = None
    sender = None
    bcc = []
    username_to = get_name_from_email(email_obj.recipient)
    user_to = get_object_or_None(
        User, username=username_to)
    user_from = get_first_object_or_None(
        User, email=get_cleaned_email(email_obj.sender))

    if 'BCC' in msg:
        bcc = msg['BCC'].split(',')
        bcc = [x.strip() for x in bcc]

    if user_to:
        profile_to = user_to.get_profile()
        if profile_to and profile_to.bcc:
            bcc.append(profile_to.bcc)
    if user_from:
        profile_from = user_from.get_profile()
        if profile_from and profile_from.bcc and profile_from.bcc not in bcc:
            bcc.append(profile_from.bcc)

    if user_to is not None and user_from is None:
        recipient = user_to.email
        sender = EmailRedirect.objects.get_or_create_back_email(
            get_cleaned_email(email_obj.sender))

    if user_from is not None and user_to is None:
        recipient = EmailRedirect.objects.get_original_from_back_email(
            get_cleaned_email(email_obj.recipient))
        sender = '%s%s' % (
            user_from.username, EmailRedirect.get_server_email_domain())

    if user_to is not None and user_from is not None:
        recipient = user_to.email
        sender = '%s%s' % (
            user_from.username, EmailRedirect.get_server_email_domain())

    if not recipient:
        smtp_server = smtplib.SMTP(
            settings.EMAIL_HOST, settings.EMAIL_PORT)
        mail_for_unknown_user.send(
            sender=EmailLog, instance=email_obj, original_msg=msg,
            mail_sender_email=sender,
            send_email=send_email, smtp_sendmail=smtp_server.sendmail
        )
        smtp_server.quit()
        return None

    if recipient is None or sender is None:
        raise NotImplementedError("Sender (%s) or recipient (%s) is not set" % (
            sender, recipient))

    del msg['From']
    del msg['To']
    del msg['Reply-To']
    msg['From'] = sender
    msg['To'] = recipient

    logger.debug(
        '\nin : %35s --> %-35s'
        '\nout: %35s --> %-35s\n' % (
            orig_from, orig_to, msg['From'], msg['To'])
    )

    if 'BCC' in msg:
        del msg['BCC']
    # Send the message via local SMTP server.
    if send_email and user_to.email and not is_local_email(user_to.email):
        smtp_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        if settings.EMAIL_USE_TLS:
            raise NotImplementedError("using TLS is not supported")
        try:
            smtp_server.sendmail(sender, recipient, msg.as_string())
            if bcc:
                msg['BCC'] = ','.join(bcc)
                smtp_server.sendmail(sender, bcc, msg.as_string())
        except smtplib.SMTPRecipientsRefused as e:
            logger.error("\nCan't send mail to recipients: %s. Original recipients: %s" % (
                e.recipients, orig_to))
            logger.debug(traceback.format_exc())
            raise
        except Exception as e:
            logger.error('\nUnknown error.')
            logger.debug(traceback.format_exc())
            raise
        smtp_server.quit()
    else:
        msg['BCC'] = ','.join(bcc)
    return msg


def save_email_object(raw_email, send_email=False):

    parser = email.FeedParser.FeedParser()
    for msg_line in raw_email:
        parser.feed(msg_line)
    msg = parser.close()

    if is_outgoing(msg) and not PROCESS_OUTGOING_EMAILS:
        return

    if 'BCC' in msg:
        bcc = msg['BCC'].split(',')
        bcc = [x.strip() for x in bcc]
        if SELF_ADDRESS in bcc:
            bcc.remove(SELF_ADDRESS)
            del msg['BCC']
            msg['BCC'] = ','.join(bcc)

    dest_document_body = msg.as_string()

    # walk through email body
    for part in msg.walk():
        # read message body
        content_type = part.get_content_type()

        if content_type == 'text' or content_type == 'text/plain':
            dest_document_body = part.get_payload(decode=True)

        # message with text will get higher priority than html
        if content_type == 'text/html' and not dest_document_body:
            dest_document_body = part.get_payload(decode=True)

    email_obj = EmailLog.objects.create(
        sender=msg['From'],
        recipient=msg['To'],
        subject=msg['Subject'],
        raw_body=dest_document_body,
        message_id=msg['Message-ID'] or "",
        in_reply_to=msg['In-Reply-To'] or ""
    )

    email_obj.raw_email.save(str(uuid.uuid4()), ContentFile(msg.as_string()))

    # saving attachments
    attaches = get_attachments(msg)
    for (file_name, content, mimetype) in attaches:
        file_name = pytils.translit.translify(unicode(file_name), strict=False)
        file_name = ''.join([c for c in file_name if ord(c) <= 128])
        file_name = file_name or 'bad_name'
        email_attach = EmailAttachment(email_log=email_obj)
        email_attach.attachment.save(file_name, ContentFile(content))

    orig_from = msg['From']
    orig_to = msg['To']

    if ',' in email_obj.recipient:
        # TODO few recipients not implemented
        recipients = email_obj.recipient.split(',')
        for recipient in recipients:
            recipient = recipient.strip()
            if not recipient or not is_project_recipient(recipient):
                continue
            email_obj.recipient = recipient
            msg = send_them(
                email_obj, msg, send_email) or msg
    else:
        msg = send_them(email_obj, msg, send_email)
    return msg


def main(raw_email):
    save_email_object(raw_email, send_email=True)


if __name__ == "__main__":
    email_input = sys.stdin.readlines()
    main(email_input)
