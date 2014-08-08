# encoding: utf-8
import logging

from django.core.management import BaseCommand

from permalink_adder import adder


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Add permalinks to text."""

    def handle(self, *args, **kwargs):
        adder.permalink_adder()
