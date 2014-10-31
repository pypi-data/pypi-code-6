from django.core.management.base import BaseCommand

import os
from collections import OrderedDict

from ._code_stats import SummaryPresenter


class Command(BaseCommand):

    help = "Report something nice for you."

    def handle(self, *args, **options):

        targets = self.sniff()
        output = SummaryPresenter.summarize(targets)
        self.stdout.write(output)

    def sniff(self):
        targets = OrderedDict()
        targets['View'] = []
        targets['Model'] = []
        targets['Route'] = []
        targets['Other Modules'] = []
        targets['JS'] = []
        targets['Coffee'] = []
        for dname, subdirs, fnames in os.walk('.'):
            for fname in fnames:
                path = os.path.join(dname, fname)
                if os.path.isfile(path):
                    category = self.categorize(path)
                    if category:
                        if not category in targets:
                            targets[category] = []
                        targets[category].append(path)
        return targets

    def categorize(self, fname):
        ignored_directory = 'node_modules'
        if ignored_directory in fname:
            return ''
        if fname.endswith('views.py'):
            return 'View'
        elif fname.endswith('models.py'):
            return 'Model'
        elif fname.endswith('urls.py'):
            return 'Route'
        elif fname.endswith('.py'):
            return 'Other Modules'
        elif fname.endswith('.js'):
            return 'JS'
        elif fname.endswith('.coffee'):
            return 'Coffee'
        else:
            return ''
