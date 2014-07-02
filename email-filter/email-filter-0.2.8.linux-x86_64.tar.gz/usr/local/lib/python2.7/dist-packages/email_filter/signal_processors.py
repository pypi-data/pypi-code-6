# -*- coding: utf-8 -*-
import smtplib

from django.conf import settings

from email_filter.models import EmailRedirect, get_name_from_email


def notify_unknown_user(
        sender, instance, original_msg, mail_sender_email, send_email, smtp_sendmail, **kwargs):
    smtp_server = smtplib.SMTP(
        settings.EMAIL_HOST, settings.EMAIL_PORT)
    email_from = 'noreply%s' % EmailRedirect.get_server_email_domain()
    msg_format = (
        'To: {sender}\nFrom: {email_from}\nSubject: undelivered mail \n\n'
        'User with username {username} not exists! \n\n')
    sender = sender_email or original_msg['From']
    username_to = get_name_from_email(instance.recipient)
    msg = msg_format.format(
        sender=sender,
        email_from=email_from,
        username=username_to)
    smtp_server.sendmail(email_from, sender, msg)
    smtp_server.quit()
