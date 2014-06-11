from subprocess import call
from landslide.generator import Generator
import os
import time

def dirname():
    return os.path.dirname(os.path.realpath(__file__))

def file_in_dir(filename):
    return os.path.join(dirname(), filename)

def open_slides():
    cmd = "landslide -o out.html {0}".format(file_in_dir('slides.md'))
    slides_path = file_in_dir('slides.md')
    output_path = 'pipped-slides.html'
    Generator(slides_path, **{
        'embed': True,
        'relative': True,
        'destination_file': output_path
    }).execute()
    call(['open', output_path])

    # sleep to let the browser open
    time.sleep(1)

    call(['rm', output_path])

def run():
    open_slides()
