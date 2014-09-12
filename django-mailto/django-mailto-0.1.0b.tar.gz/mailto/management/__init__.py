# -*- coding: utf-8 -*-
import logging

from django.conf import settings

from django.db.models.signals import post_syncdb
from django.dispatch import receiver

import mailto.models


log = logging.getLogger(__name__)


@receiver(post_syncdb, sender=mailto.models)
def register_initial_mails(sender, **kwargs):
    for slug in getattr(settings, 'MAILTO_MAILS', []):
        m = mailto.models.Mail.register(slug)