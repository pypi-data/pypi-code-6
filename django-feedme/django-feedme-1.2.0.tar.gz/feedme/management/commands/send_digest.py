# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from feedme import digest


class Command(BaseCommand):
    help = 'Send Digest'

    def handle(self, *args, **options):
        digest.send_digest()
