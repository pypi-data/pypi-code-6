from django.template import loader, Context
from django.conf import settings
from django.contrib.auth.models import User

from mailqueue.models import MailerMessage as MailMessage

from .models import FeedItem


def send_digest():
    text_template = loader.get_template('feedme/mail/digest.txt')
    html_template = loader.get_template('feedme/mail/digest.html')
    subject = 'Daily FeedMe Digest'

    for user in User.objects.all():
        items = FeedItem.objects.my_feed_items(user).yesterday()
        if items:
            context_dict = {'items': items}
            context = Context(context_dict)
            msg = MailMessage(subject=subject)
            msg.to_address = user.email
            msg.from_address = settings.FEEDME_FROM_EMAIL
            msg.content = text_template.render(context)
            msg.html_content = html_template.render(context)
            msg.app = 'Feed Me'
            msg.save()

