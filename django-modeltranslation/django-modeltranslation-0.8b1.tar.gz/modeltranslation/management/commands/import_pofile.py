# -*- coding: utf-8 -*-
from optparse import make_option
import polib

# from django import VERSION
from django.core.management.base import BaseCommand, CommandError
from django.db.models.loading import get_model
# from django.utils import translation

# from modeltranslation import settings as mt_settings


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-f', '--file', dest='filename', type='string',
            help='Po file to import.'),
    )
    help = 'Import modeltranslation field values from po file.'
    # leave_locale_alone = mt_settings.LOADDATA_RETAIN_LOCALE  # Django 1.6

    # def __init__(self):
    #     super(Command, self).__init__()
    #     if mt_settings.LOADDATA_RETAIN_LOCALE and VERSION < (1, 6):
    #         from django.utils import translation
    #         self.locale = translation.get_language()

    def handle(self, *args, **options):
        # if self.can_import_settings and hasattr(self, 'locale'):
        #     translation.activate(self.locale)

        if not options['filename']:
            raise CommandError('Option --file must be specified.')
        filename = options['filename']

        po = polib.pofile(filename)

        for entry in po:
            for occurrence in entry.occurrences:
                app_label, model_name, fieldname = occurrence[0].split('.')
                obj_id = occurrence[1]
                model = get_model(app_label, model_name)
                obj = model.objects.get(pk=obj_id)
                setattr(obj, fieldname, entry.msgstr)
                obj.save()
