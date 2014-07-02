# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from feedme import digest


class Command(BaseCommand):
    """
    Management command to send the daily digest.  Typically
    called by Celery.
    """
    help = 'Send Digest'

    def handle(self, *args, **options):
        digest.send_digest()
