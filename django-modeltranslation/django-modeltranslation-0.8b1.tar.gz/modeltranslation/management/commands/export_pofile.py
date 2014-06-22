# -*- coding: utf-8 -*-
from datetime import datetime
from optparse import make_option
import os
import polib

# from django import VERSION
from django.db.models.fields import CharField, TextField
from django.core.management.base import BaseCommand, CommandError
# from django.utils import translation

# from modeltranslation import settings as mt_settings
from modeltranslation.translator import translator


def get_value(trans_fields, obj, lang='en'):
    msg = getattr(obj, get_translation_field_by_language(trans_fields, lang).name, u'')
    return unicode(msg) if msg is not None else u''


def get_translation_field_by_language(translation_fields, language):
    for field in translation_fields:
        if field.language == language:
            return field


def filter_translation_fields(translation_fields, languages):
    return [f for f in translation_fields if f.language in languages and isinstance(
        f, (CharField, TextField,))]


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-f', '--from-locale', dest='from_locale', type='string',
            help='From locale. Becomes msgid in po file.'),
        make_option(
            '-t', '--to-locale', dest='to_locale', type='string',
            help='To locale. Becomes msgstr in po file. Also used as name of created file.'),
    )
    help = 'Export modeltranslation field values to po file.'
    # leave_locale_alone = mt_settings.LOADDATA_RETAIN_LOCALE  # Django 1.6

    # def __init__(self):
    #     super(Command, self).__init__()
    #     if mt_settings.LOADDATA_RETAIN_LOCALE and VERSION < (1, 6):
    #         from django.utils import translation
    #         self.locale = translation.get_language()

    def handle(self, *args, **options):
        # if self.can_import_settings and hasattr(self, 'locale'):
        #     translation.activate(self.locale)

        if not options['from_locale']:
            raise CommandError('Option --from-locale must be specified.')
        to_locale = options['to_locale']
        if not options['to_locale']:
            raise CommandError('Option --to-locale must be specified.')
        from_locale = options['from_locale']

        #print translation.get_language()
        now = datetime.now().strftime('%Y-%m-%d %H:%M%Z')

        po = polib.POFile()
        po.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'you@example.com',
            'POT-Creation-Date': '%s' % now,
            'PO-Revision-Date': '%s' % now,
            'Last-Translator': 'you <you@example.com>',
            'Language-Team': '%s' % options['to_locale'],
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

        # for available_language in mt_settings.AVAILABLE_LANGUAGES:
        #     print available_language

        # target_languages = (
        #     [options['to_locale']] if options['to_locale'] else mt_settings.AVAILABLE_LANGUAGES)
        # print target_languages

        for model, trans_opts in translator._registry.items():
            for obj in model.objects.all():
                for trans_fields in trans_opts.fields.values():
                    filtered_trans_fields = filter_translation_fields(
                        trans_fields, [from_locale, to_locale])

                    for trans_field in filtered_trans_fields:
                        msgid = get_value(filtered_trans_fields, obj, lang=from_locale)
                        msgstr = get_value(filtered_trans_fields, obj, lang=to_locale)
                        if msgid:
                            if trans_field.language == to_locale:
                                entry = polib.POEntry(
                                    msgid=msgid,
                                    msgstr=msgstr,
                                    occurrences=[(str(trans_field), obj.pk)]
                                )
                                po.append(entry)
                        # else:
                        #     print('Source language empty, skipped %s (%s)' % (obj, obj.pk))

        po.save(os.path.join(os.getcwd(), '%s.po' % to_locale))
