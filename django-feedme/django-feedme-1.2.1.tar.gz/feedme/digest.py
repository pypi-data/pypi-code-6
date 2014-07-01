"""
Django Feedme

Digest.py

Author: Derek Stegelman
"""
from django.template import loader, Context
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from .models import FeedItem


def send_digest():
    """
    Send the daily digest for all users.  This sends
    both a .txt and .html version of the email.  
    :return:
    """
    text_template = loader.get_template('feedme/mail/digest.txt')
    html_template = loader.get_template('feedme/mail/digest.html')
    subject = 'Daily FeedMe Digest'

    for user in User.objects.all():
        items = FeedItem.objects.my_feed_items(user).yesterday()
        if items:
            context_dict = {'items': items}
            context = Context(context_dict)
            from_email = getattr(settings, 'FEEDME_FROM_EMAIL', 'test@test.com')
            text_content = text_template.render(context)
            html_content = html_template.render(context)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

