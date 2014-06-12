from subprocess import call
from landslide.generator import Generator
import os
import time

description = """
%prog [slides - print the slides | links - print the links]
"""


def dirname():
    return os.path.dirname(os.path.realpath(__file__))


def file_in_dir(filename):
    return os.path.join(dirname(), 'data', filename)


def open_slides():
    slides_path = file_in_dir('slides.md')
    output_path = 'pipped-slides.html'
    Generator(slides_path, **{
        'embed': True,
        'relative': True,
        'destination_file': output_path,
        'theme': file_in_dir('avalanche'),
    }).execute()
    call(['open', output_path])


def run():
    print("publising pip packages - nyc python talk on 2014-06-12")
    print("code available at https://github.com/brianc/publishing-pip-packages")
    open_slides()
    print('i created a file: ./pipped-slides.html You might want to delete it....')
