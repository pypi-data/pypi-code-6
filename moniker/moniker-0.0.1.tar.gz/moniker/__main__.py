# -*- coding: utf-8 -*-
import re
import json
import os
import sys

from os.path import basename
from argparse import ArgumentParser

from .__version__ import __version__, __build__

from .moniker import tree_walk

try:
    from pygments import highlight
    from pygments.lexers.web import JsonLexer
    from pygments.formatters import Terminal256Formatter
    from pygments.styles import STYLE_MAP as pygments_builtins
except:
    # No color for you
    pass

def main():
    '''Main Entry point'''
    version = ' '.join([__version__, __build__])
    parser = ArgumentParser(
        prog='moniker',
        description='Simple batch file renaming tool.',
    )
    parser.add_argument(
        '-V', '--version', action='version',
        version="%s v%s" % (basename(sys.argv[0]), version))

    # Not Yet Implemented
    parser.add_argument(
        '-t', '--test', action='store_true',
        help='Run test in-place without renaming',
    )

    # Not Yet Implemented
    parser.add_argument(
        '-f', '--force', action='store_true',
        help='Do it by force, no checks.',
    )

    # Not Yet Implemented
    parser.add_argument(
        '-r', '--recursive', action='store_true',
        help='Recursive renaming',
    )

    # Not Yet Implemented
    parser.add_argument(
        '-i', '--interactive', action='store_true',
        help='Go into interactive mode',
    )
    parser.add_argument(
        'directory',
        help='target directory'
    )
    parser.add_argument(
        'pattern',
        type=str,
        help='glob pattern to match'
    )
    parser.add_argument(
        'replace',
        help='glob pattern to match'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        raise IOError

    filetree = tree_walk(args.directory, args.pattern, args.replace)
    jsontree = json.dumps(filetree, indent=2, sort_keys=True, separators=(', ', ': '))
    try: jsontree = highlight(jsontree, JsonLexer(), Terminal256Formatter(style='autumn'))
    except: pass

    print(jsontree)

if __name__ == '__main__':
    sys.exit(main())
