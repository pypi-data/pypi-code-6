# -*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand

from cms import api

try:
    from djangocms_snippet.models import Snippet as OldSnippet
    from djangocms_snippet.cms_plugins import SnippetPlugin as OldSnippetPlugin
except ImportError:
    OldSnippet, OldSnippetPlugin = None

from ...cms_plugins import Snippet


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--keep',
            action='store_true',
            dest='keep',
            default=False,
            help='Keep old snippets after migration'
        ),
    )

    def handle(self, *args, **options):
        if not OldSnippet or not OldSnippetPlugin:
            raise Exception("djangocms-snippet must still be installed for the migration to work!")

        for snippet in OldSnippet.objects.all():
            for ptr in snippet.snippetptr_set.all():
                new_plugin = api.add_plugin(ptr.placeholder, Snippet, ptr.language, target=ptr, position='right')
                new_plugin.content = ptr.snippet.html
                new_plugin.save()
                ptr.delete()

            if not options['keep']:
                snippet.delete()
