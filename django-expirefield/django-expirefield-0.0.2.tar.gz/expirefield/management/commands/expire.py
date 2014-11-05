from django.core.management.base import BaseCommand, \
    CommandError, NoArgsCommand
from expirefield.fields import ExpireField
from django.db import models
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Crawl through database and remove rows from tables with ExpireFields'

    def handle(self, *args, **options):
        # get all models that have an ExpireField
        ms = [m for m in models.get_models() 
             if any( type(f) is ExpireField for f in m._meta.fields)]
        # asume parameter is in hours
        for m in ms:
            self.stdout.write('expiring ' + m._meta.verbose_name + '\n')
            # get first expirefield, so if multiple are defined, only
            # the first is used
            field = next(f for f in m._meta.fields 
                        if type(f) is ExpireField )
            delta_t = field.duration
            filter_args = {'{0}__{1}'.format(field.name, 'lt'): 
                           (datetime.now() - delta_t),}
            # delete all the old objects
            q = m.objects.filter(**filter_args)
            q.delete()
