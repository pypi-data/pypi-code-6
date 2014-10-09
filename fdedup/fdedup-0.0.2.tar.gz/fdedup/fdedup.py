#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import hashlib

import os
import itertools


def find_files(root):
    def join(path, _, files):
        return itertools.imap(os.path.join,
                              itertools.cycle([path]),
                              files)

    return itertools.chain(*itertools.starmap(join, os.walk(root)))


def find_candidates(paths, func):
    candidates = {}
    for path in paths:
        candidates.setdefault(func(path), []).append(path)
    return (v for v in candidates.values() if len(v) > 1)


def file_md5(path):
    with open(path, 'rb') as f:
        md5 = hashlib.md5()
        md5.update(f.read())
    return md5.digest()


def find_duplicates(root):
    paths = find_files(root)
    candidates = find_candidates(paths, os.path.getsize)

    duplicates = []
    for paths in candidates:
        duplicates.extend(list(find_candidates(paths, file_md5)))

    return duplicates


def main():
    parser = argparse.ArgumentParser(
        description='Find file duplicates.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('paths', nargs='+', metavar='PATH', help='paths to scan for duplicates')
    opts = parser.parse_args()

    for path in opts.paths:
        print find_duplicates(path)


if __name__ == '__main__':
    main()