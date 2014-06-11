from subprocess import call
from landslide.generator import Generator
import os
import sys
import time
from optparse import OptionParser

description = """
%prog [slides - print the slides | links - print the links]
"""

def parse_options():
    parser = OptionParser(
        usage="%prog [options] slides|links",
        description=description
    )

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    return options, args

def dirname():
    return os.path.dirname(os.path.realpath(__file__))

def file_in_dir(filename):
    return os.path.join(dirname(), 'data', filename)

def open_slides():
    cmd = "landslide -o out.html {0}".format(file_in_dir('slides.md'))
    slides_path = file_in_dir('slides.md')
    output_path = 'pipped-slides.html'
    Generator(slides_path, **{
        'embed': True,
        'relative': True,
        'destination_file': output_path,
        'theme': file_in_dir('avalanche'),
    }).execute()
    call(['open', output_path])

    # sleep to let the browser open
    time.sleep(1)

    call(['rm', output_path])

def run():
    options, args = parse_options()
    if args[-1] == 'slides':
        open_slides()
    else:
        print('do it')
