#!/usr/bin/env python

"""
get the human-form of the name of the final path segment in a url:

xclip -o | sed 's/_//' | sed 's/.html//'
"""

import argparse
import sys
import urlparse

def url2txt(url, strip_extension=True, replacements=(('_', ' '),)):
    """gets the text equivalent of a URL"""

    # parse the url
    parsed = urlparse.urlparse(url)

    # process the path, if available
    path = parsed.path.rstrip('/')
    if path:
        text = path.split('/')[-1]
        if strip_extension:
            # strip the extension, if desired
            text = text.split('.', 1)[0]
    else:
        # otherwise go with the hostname
        text = parsed.hostname

    # replace desired items
    for item, replacement in replacements:
        text = text.replace(item, replacement)

    return text


def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('urls', metavar='url', nargs='+',
                        help="URLs to convert")
    options = parser.parse_args(args)

    # convert urls
    for url in options.urls:
        print (url2txt(url))


if __name__ == '__main__':
    main()
