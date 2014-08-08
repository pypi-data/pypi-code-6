# encoding: utf-8
from permalink_adder.helpers import add_permalinks
from django.conf import settings


def permalink_adder():
    for config_set in settings.PERMALINK_ADDER_SETTINGS:
        app = config_set['app']
        model_name = config_set['model_name']
        fields = config_set['fields']
        words = config_set['words']
        url = config_set['url']
        dry_run = config_set['dry_run']
        add_permalinks(app, model_name, fields, words, url, dry_run)
