from django.core.management.base import BaseCommand
from kvtags.utils import import_tags_csv


class Command(BaseCommand):
    """Provides command interface to utils.import_tags_csv"""
    args = '<csv_file>'
    help = 'Imports tags from csv file to database'

    def handle(self, *args, **options):
        with open(args[0], 'rb') as csv_file:
            import_tags_csv(csv_file)
