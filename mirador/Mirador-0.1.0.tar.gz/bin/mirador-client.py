#!/usr/bin/env python
# mirador command line interface
# @author nickjacob (nick@mirador.im)
#####
from optparse import OptionParser
from mirador import MiradorClient
from os import getenv as _genv
import sys
import re
import json

# a basic url regexp; just want to
# check what the user is sending us
URL_RXP = re.compile(r'^https?:\/\/')


def err_print(msg):
    sys.stderr.write(msg + "\n")


def die(msg):
    sys.exit(msg)


def format_plaintext(res, delimiter):
    return "{name}{d}{safe}{d}{value}".format(
        name=res.name,
        safe=res.safe,
        value=res.value,
        d=delimiter
    )


def format_json(res):
    return json.dumps({
        'name': res.name,
        'safe': res.safe,
        'value': res.value,
    })


def classify_all(args, force_url=False, api_key=None):
    mc = MiradorClient(api_key)

    if force_url:
        return mc.classify_urls(*args)
    else:
        files, urls = [], []
        for x in args:
            if URL_RXP.match(x):
                urls.append(x)
            else:
                files.append(x)

        return (mc.classify_files(*files)
                + mc.classify_urls(*urls))


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        '-k', '--api-key', dest='api_key',
        help='your mirador.im API key')
    parser.add_option(
        '-u', '--urls', dest='is_url',
        help='run arguments as urls', default=False)
    parser.add_option(
        '-j', '--json', dest='is_json',
        help='format output as json'
    )
    parser.add_option('-H', '--header', dest='header',
                      help='show header in plaintext output')

    (options, args) = parser.parse_args()

    api_key = options.api_key or _genv('MIRADOR_API_KEY', None)
    if not api_key:
        die("api key not provided through options or $MIRADOR_API_KEY")

    results = classify_all(args, force_url=options.is_url, api_key=api_key)

    if options.is_json:
        print json.dumps({'results': map(format_json, results)})
    else:

        if options.header:
            print options.delimiter.join(
                ['name', 'safe', 'value'])

        for res in results:
            print format_plaintext(res, options.delimiter)
