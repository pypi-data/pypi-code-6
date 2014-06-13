#!/usr/bin/python

"""melody-dl
Usage:
  melody-dl [--template=<template>] [--base-dir=<dir>]
              [--quiet] [--full-album] <url>
  melody-dl (-h | --help)
  melody-dl (--version)

Options:
  -h --help                 Show this screen.
  -v --version              Show version.
  -q --quiet                Dont display anything to the screen.
  -t --template=<template>  Output filename template.
                            [default: %{artist}/%{album}/%{track} - %{title}]
  -d --base-dir=<dir>       Base location of which all files are downloaded
  -f --full-album           Download only if all tracks are availiable
"""


import os

from docopt import docopt
import progress

from melody_dl.MelodyDL import MelodyDL



class CLI():
    def main(self):
        arguments = docopt(__doc__, version='melody-dl 0.1')

        if (arguments):
            if arguments['--quiet']:
                progress_callback = None

            else:
                self.bar = progress.ProgressBar("[{progress}] {percentage:.0f}%", width=30)
                progress_callback = self.update_status_bar

            if arguments['<url>']:
                url = arguments['<url>']

            if url:
                base_dir = arguments['--base-dir']

                if arguments['--template']:
                    template = arguments['--template']

                # if arguments['--full-album'] and not album['full']:
                #     print "Full album not availiable. Skipping.."


                mdl = MelodyDL(url, progress_callback, base_dir, template)
                mdl.download()

        else:
            print __doc__


    def update_status_bar(self, progress):
            percent = progress['percent'] * 100

            self.bar.reset()
            self.bar.update(percent)
            self.bar.show()
