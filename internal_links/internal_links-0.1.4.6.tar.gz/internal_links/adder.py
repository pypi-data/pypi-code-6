# encoding: utf-8
from internal_links.helpers import add_links
from django.conf import settings


def link_adder(dry_run=True):
    for config_set in settings.INTERNAL_LINKS_SETTINGS:
        add_links(dry_run=dry_run, **config_set)
