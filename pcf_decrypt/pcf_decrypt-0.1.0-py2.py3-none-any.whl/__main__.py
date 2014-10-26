# coding=utf-8

import os
import re
import sys
import shlex
import binascii
from collections import Container

import argparse

from six import string_types, print_

from . import decrypt, PcfDecryptionError, DecodeError


PCF_ENCFIELD_RE = re.compile(r'^enc_([^=]+)\s*=([^$]+)$')


class StoreArg(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        files = set()
        hashes = set()
        for key, value in values:
            if key == 'file':
                files.add(value)
            elif key == 'hash':
                hashes.add(value)
            else:
                raise ValueError('unkown key %r returned for value %r'
                                 % (key, value))

        setattr(namespace, 'files', list(files))
        setattr(namespace, 'hashes', list(hashes))


def _file_or_hash(arg):
    if os.path.exists(arg):
        return ('file', os.path.realpath(arg))

    try:
        data = binascii.a2b_hex(arg)
        if len(data) < 48:
            raise argparse.ArgumentTypeError(
                '%r is not a long enough hash to be an encrypted password'
                % arg
            )
        return ('hash', data)
    except DecodeError:
        pass

    raise argparse.ArgumentTypeError('%r is not a file or a hash' % arg)


def run_args(args):
    if args.hashes:
        for data in args.hashes:
            try:
                print_(decrypt(data))
            except PcfDecryptionError as e:
                print_(
                    'Failed to decrypt %r, %s' % (data, e.message),
                    file=sys.stderr
                )

    if args.files:
        for path in args.files:
            basename = os.path.splitext(os.path.basename(path))[0]

            with open(path, 'r') as fp:
                lines = fp.read().splitlines()

            fields = filter(None, map(PCF_ENCFIELD_RE.match, lines))
            for field, hexhash in (match.groups() for match in fields):
                try:
                    plaintext = decrypt(hexhash)
                except PcfDecryptionError as e:
                    print_("%s:%s:Error %s" % (basename, field, e.message))
                else:
                    print_("%s:%s:%s" % (basename, field, plaintext))


def get_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if argv and isinstance(argv, string_types):
        argv = shlex.split(argv)

    if argv and not isinstance(argv, Container):
        raise TypeError(
            '%r is not a container or a string: %r'
            % (type(argv).__name__, argv)
        )

    parser = argparse.ArgumentParser(
        prog='pcf_decrypt',
        description='Decrypt encryped passwords in Cisco pcf files',
        epilog="""Arguments can either be a pcf file with at least one
        enc_FIELD field within to decrypt or an encrypted hash to decrypt. If
        any hashes are present (determined if the operating system say it's not
        a path to a file and can be successfully decoded from a hex string to a
        byte array), they will be outputted in order presented first, followed
        by any files in the form: filename:FIELD:plaintext"""
    )

    parser.add_argument(
        'args',
        action=StoreArg,
        nargs='+',
        type=_file_or_hash,
        help='File to parse or hash to decode',
        metavar='file_or_hash'
    )

    return parser.parse_args(argv)


def main(argv=None):
    run_args(get_args(argv))

if __name__ == '__main__':
    main()
