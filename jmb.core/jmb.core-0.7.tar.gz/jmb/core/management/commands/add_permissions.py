# coding: utf-8
"""
Command to add new permissions
================================

scopo
--------

è facile aggiungere permessi ad un modello in modo che vengano creati al syncdb. 
Aggiungere però permessi **dopo** questo momento crea difficoltà in quanto non 
vengno più creati. Questo comando permette di creare i permessi in modo non 
legato al sync del db.

Examples:: 

  dj add_permissions # aggiunge tutti i permessi mancanti in 'Permission'
  dj add_permissions acomea.contact  # aggiunge i permessi mancanti solo dell'applicazione 'acomea.contact'
  dj add_permissions contact # uguale al precedente
  dj add_permissions contact Role # aggiunge i permessi mancanti del modello 'Role' 


"""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_app, get_models
from django.db.models.loading import get_model
from django.utils.translation import ugettext as _

from optparse import make_option

class Command(BaseCommand):
    """
    command to add new permissions
    """
    args = 'nothing, application and model'
    help = 'A way to add new permissions'

    def handle(self, *args, **opts):
        if not args:
            # get all project content types
            ctypes = ContentType.objects.all() 
            for ctype in ctypes:
                # get model
                model = ctype.model_class()
                if model:
                    # set model permissions
                    self.set_permissions(model)

        elif len(args) == 1:
            application_name = args[0].split('.')[-1]
            application = get_app(application_name)
            models = get_models(application)
            for model in models:
                self.set_permissions(model)

        elif len(args) == 2:
            application_name = args[0].split('.')[-1]
            model_name = args[1]
            model = get_model(application_name, model_name)
            if model:
                self.set_permissions(model)
            else:
                raise CommandError("Model with label %s could not be found" % model_name)
        else:
            print 'many args'

    def set_permissions(self, model):
        permissions = model._meta.permissions
        ctype = ContentType.objects.get_for_model(model)
        for permission in permissions:
            codename=permission[0]
            name=permission[1]

            try:
                p, created = Permission.objects.get_or_create(
                    codename=codename, content_type__pk=ctype.id,
                    defaults={'name': name, 'content_type': ctype}
                )
                if created:
                    print "%s: created" % p
                else:
                    print "%s: already exist" % p
            except Exception, e:
                print "%s: %s" (p, e)
