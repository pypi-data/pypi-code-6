# encoding: utf-8
import logging

from django.core.management import BaseCommand
from optparse import make_option

from permalink_adder import adder


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Add permalinks to text."""

    option_list = BaseCommand.option_list + (
        make_option('-s', '--start', dest='start', default=True, action='store_false',
                    help='Start creating permalinks.'),
    )

    def handle(self, *args, **options):
        dry_run = options.get('start')
        print 'Dry run: %s' % dry_run
        adder.permalink_adder(dry_run=options.get('start'))
