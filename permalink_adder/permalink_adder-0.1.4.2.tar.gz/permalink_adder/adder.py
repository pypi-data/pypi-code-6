# encoding: utf-8
from permalink_adder.helpers import add_permalinks
from django.conf import settings


def permalink_adder():
    for config_set in settings.PERMALINK_ADDER_SETTINGS:
        add_permalinks(**config_set)
