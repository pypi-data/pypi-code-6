#!/usr/bin/env python
"""
sphinx-dehead
=============

- **Author:** Sean Wallitsch
- **Email:** sean@grenadehop.com
- **License:** MIT
- **Status:** Development
- **Python Versions:** 2.6-2.7

A script to extract the first found `<div class='section'>` from an HTML
document, then save that extracted element to it's own HTML file. Useful when
including an HTML file in another document, when you don't need all the header
junk.

Developed for including Sphinx built HTML documentation in an Octopress blog.

Usage
-----

sphinx-dehead takes a glob style input parameter, and an optional output
directory.

For example, this will dehead every HTML file in the current directory, and
save it to the default output directory, `dehead_output/`

.. code-block:: console

    $ sphinx-dehead './*.html'

While this will save it in the sibling `_docs` directory:

.. code-block:: console

    $ sphinx-dehead './*.html' -d ../_docs/

Installation
------------

sphinx-dehead can be installed with pip:

.. code-block:: console

    $ pip install sphinx-dehead

or by cloning the repository, and from the root directory calling:

.. code-block:: console

    $ python setup.py install


Public Functions
----------------

    main()
        Main script execution.

License
-------

The MIT License (MIT)

sphinx-dehead
Copyright (c) 2014 By Sean Wallitsch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

# =============================================================================
# IMPORTS
# =============================================================================

# Future Imports
from __future__ import print_function

# Standard Imports
from argparse import ArgumentParser
import codecs
from glob import glob
import os

# Third Party Imports
import bs4

# =============================================================================
# GLOBALS
# =============================================================================

__author__ = "Sean Wallitsch"
__author_email__ = "sean@grenadehop.com"
__copyright__ = "Copyright 2014, Sean Wallitsch"
__credits__ = ["Sean Wallitsch", ]
__license__ = "MIT"
__version__ = "0.2.1"
__module_name__ = "sphinx-dehead"
__short_desc__ = "A script to extract the main div section element from HTML"
__status__ = "Development"
__url__ = "http://github.com/shidarin/dehead"

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'main'
]

# =============================================================================
# PRIVATE FUNCTIONS
# =============================================================================


def _get_input_files(input_arg):
    """Returns glob output of `input_arg`"""
    # Just grab any files specified, don't mess with provided patterns.
    files = glob(input_arg)

    # But only accept files that end in html.
    return [html_file for html_file in files if html_file.endswith('html')]

# =============================================================================


def _parse_args():
    """Uses argparse to parse command line arguments"""
    parser = ArgumentParser(description=__short_desc__)
    parser.add_argument(
        "input_files",
        help="the file(s) to be converted. Will do glob style pattern matching"
    )
    parser.add_argument(
        "-d",
        "--destination",
        help="specify an output directory to save converted files to. If not "
             "provided will default to ./dehead_output/"
    )

    args = parser.parse_args()

    if not args.destination:
        args.destination = './dehead_output/'

    return args

# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================


def main():
    """Main dehead script entry"""
    args = _parse_args()

    if not os.path.exists(args.destination):
        os.makedirs(args.destination)

    for html_file in _get_input_files(args.input_files):
        print("Reading file: {0}".format(html_file))
        with codecs.open(html_file, 'rb', 'utf-8') as html:
            soup = bs4.BeautifulSoup(html.read())

        section = soup.find('div', {'class': 'section'})

        if section:
            destination = os.path.join(args.destination, html_file)

            # Remove master heading, since we'll be including it elsewhere.
            title = section.find('h1')
            if title:
                title.extract()

            print("Writing file: {0}".format(destination))
            with codecs.open(destination, 'wb', 'utf-8') as export:
                export.write(section.prettify())
        else:
            print("No 'section' found in file: {0}".format(html_file))

# =============================================================================
# RUN
# =============================================================================

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        import traceback
        print('Unexpected error encountered:')
        print(err)
        print(traceback.format_exc())
        raw_input('Press enter key to exit')
