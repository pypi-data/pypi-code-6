"""yaurtww.

Usage:
    yaurtww <filename> --dest=<target>
    yaurtww (-h | --help)
    yaurtww --version

Options:
    -h --help   Show this help message.
    --version   Show version.

"""
from __future__ import absolute_import, division, print_function

from .__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __uri__, __version__
)

__all__ = [
    "__title__", "__summary__", "__uri__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__"
]


from .manifest import Manifest
from contextlib import closing
from docopt import docopt
from os import getcwd
from os.path import abspath, expanduser
import grequests


def main():
    _default_dir = ''.join([getcwd(), 'q3ut4/'])
    arguments = docopt(__doc__, version=__version__)
    if arguments['--version']:
        print("yaurtww {0}".format(__version__))
        return

    if arguments['<filename>']:
        _target = arguments['--dest'] if arguments['--dest'] else _default_dir
        manifest_file = abspath(expanduser(arguments['<filename>']))
        manifest = Manifest(manifest_file)
        for asset in manifest.files:
            _target_file = asset.url.split('/')[-1]
            with closing(asset) as content:
                with open(''.join([_target, _target_file]), 'w') as f:
                    f.write(content)
