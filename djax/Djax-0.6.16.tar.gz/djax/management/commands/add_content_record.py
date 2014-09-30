"""
Manually adds a content record to the local cache.  Used for associating local
models with ACE content items, when the local models already exist in the database.
(This is essentially a cleanup tool, not the preferred way to operate.)
"""
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from djax.models import AxilentContentRecord
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    """
    Command class.
    """
    option_list = BaseCommand.option_list + (
        make_option('--app-label',dest='app_label',help='The app label to which the local model belongs.'),
        make_option('--local-type',dest='local_type',help='The name of the local model'),
        make_option('--local-id',dest='local_id',help='The id of the local model'),
        make_option('--content-key',dest='content_key',help='The ACE content key to associate.'),
    )
    
    def handle(self,*args,**options):
        """
        Handler method.
        """
        content_type = None
        try:
            content_type = ContentType.objects.get(app_label=options['app_label'],local_type=options['local_type'])
        except ContentType.DoesNotExist:
            raise CommandError('No such local content type.')
        
        local_model = content_type.model_class()
        if not hasattr(local_model,'ACE'):
            raise CommandError('Local model %s is not configured to be linked to ACE.' % options['local_type'])
        
        AxilentContentRecord.objects.create(local_content_type=content_type,
                                            local_id=int(options['local_id']),
                                            axilent_content_type=local_model.ACE.content_type,
                                            axilent_content_key=options['content_key'])
        
        print 'ACE content record created'
