# encoding: utf-8
from permalink_adder.helpers import add_permalinks
from django.conf import settings


def permalink_adder(dry_run=True):
    for config_set in settings.PERMALINK_ADDER_SETTINGS:
        add_permalinks(dry_run=dry_run, **config_set)
