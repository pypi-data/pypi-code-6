# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from feedme.models import Feed


class Command(BaseCommand):
    """
    Update all feed objects manually.
    """
    help = 'Update all feeds'

    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            feed._update_feed()
