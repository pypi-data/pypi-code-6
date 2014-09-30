"""
Scrubs unaffiliated local objects: those that have an ACEContent model,
but are not addressed by AxilentContentRecords.
"""
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from djax.models import AxilentContentRecord
from django.contrib.contenttypes.models import ContentType
import sys

class Command(BaseCommand):
    """
    Command class.
    """
    option_list = BaseCommand.option_list + (
        make_option('--app-label',dest='app_label',help='The app label of the local model to scrub.'),
        make_option('--local-type',dest='local_type',help='The name of the local content type to scrub.'),
    )
    
    def handle(self,*args,**options):
        """
        The handler method.
        """
        content_type = None
        try:
            content_type = ContentType.objects.get(app_label=options['app_label'],
                                                   local_type=options['local_type'])
        except ContentType.DoesNotExist:
            raise CommandError('%s content type does not exist.' % options['local_type'])
        
        local_model = content_type.model_class()
        
        affiliated_ids = [record.local_id for record in local_type.axilent_content_records.all()]
        
        unaffiliated_models = local_model.objects.exclude(pk__in=affiliated_ids)
        
        print 'This will delete',unaffiliated_models.count(),options['local_type'],'objects.  Type "yes" to proceed or anything else to abort.'
        
        while True:
            choice = raw_input().lower()
            if choice == 'yes':
                [unaffiliated_model.delete() for unaffiliated_model in unaffiliated_models]
                print 'Models deleted'
            else:
                print 'Aborting'
                sys.exit(0)
