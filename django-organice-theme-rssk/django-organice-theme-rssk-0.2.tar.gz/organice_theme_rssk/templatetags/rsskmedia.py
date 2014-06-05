__author__ = 'Peter Bittner <django@bittner.it>'

from django import template
from django.template.defaultfilters import stringfilter
from os import listdir
from os.path import dirname, join, realpath, sep
from random import randrange

register = template.Library()

@register.filter
@stringfilter
def random_image(folder_name):
    """Return a random JPG image URI path from a directory holding static files in this app"""
    folder_path = realpath(dirname(__file__) + sep + '..' + sep + folder_name)
    files = [f for f in listdir(folder_path) if f[-4:].lower() == '.jpg']
    uri_path = join(folder_name, files[randrange(len(files))])
    return uri_path
