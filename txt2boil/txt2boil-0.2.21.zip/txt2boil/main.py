"""Update the boilerplate in source code.

We do so according to a series of marker comments found through
regexs.

If --in-place is specified then the files are updated in place, if not
then they are printed to stdout.

"""

import argparse
import collections
import sys
import textwrap
import os
from langs import *
from version import version


def main():
    """The main method."""

    global ext_lang

    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog)
    parser.add_argument('-i', '--in-place', action='store_true',
                        help='modify files inplace')
    parser.add_argument('files', metavar='FILES', nargs='*',
                        help='the files to process')
    parser.add_argument('--version', action='version', version=version)
    parser.add_argument('--langs', action='store_true',
                        help='print out all the supported languages')
    args = parser.parse_args()

    # Print the current set of working languages.
    if args.langs:
        # Collect the languages so that they are indexed by name
        # rather than by extension.
        langs = {}
        for ext, cls in ext_lang.items():
            cls = type(cls)
            ext = '.' + ext
            if cls.__name__ in langs:
                langs[cls.__name__][1].append(ext)
            else:
                langs[cls.__name__] = (cls.__doc__, [ext])

        # Begin output
        parser.print_usage()
        sys.stdout.write('\n')
        sys.stdout.write(textwrap.fill(textwrap.dedent("""\
        The following languages are supported:
        """)) + '\n')
        for l in sorted(langs.keys()):
            out = langs[l][0] + ' (' + ', '.join(langs[l][1]) + ')'

            prefix2 = ' '.join([''] * 20)
            prefix1 = prefix2[:2] + l + prefix2[2+len(l):]

            wrapped = textwrap.fill(out, initial_indent=prefix1,
                                    subsequent_indent=prefix2)
            
            sys.stdout.write(wrapped + '\n')

        parser.exit(0)          # Exit once we're done

    for fname in args.files:
        # load the file
        with open(fname) as f:
            text = f.read()

        # generate the new output according to the language
        _, ext = os.path.splitext(fname)
        text = ext_lang[ext].gen(text)

        # emit the output
        if args.inplace:
            with open(fname, 'w') as f:
                f.write(text)
        else:
            sys.stdout.write(text)


description = __doc__
epilog = ''
ext_lang = collections.defaultdict(Unknown)
ext_lang.update({
    'c': C(),
    'cc': CXX(),
    'cpp': CXX(),
    'java': Java(),
    'py': Python(),
    'rkt': Racket(),
})

if __name__ == '__main__':
    main()
