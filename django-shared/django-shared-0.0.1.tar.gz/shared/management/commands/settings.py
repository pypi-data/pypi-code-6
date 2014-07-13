from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from pprint import pformat


class Command(BaseCommand):
    args = '<setting>'
    help = 'Outputs the value of the given setting name'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please enter exactly one setting name!')

        name = args[0]
        if hasattr(settings, name):
            self.stdout.write(pformat(getattr(settings, name), indent=4, width=160))
        else:
            self.stderr.write('no setting with name %s available!' % name)
