#!/usr/bin/env python3

from core import petrify, rehydrate, IGNORABLES
from shutil import rmtree
from pathlib import Path

def main():

    target = Path('service_skeleton')
    if target.exists():
        rmtree(str(target))

    replacements = {
        'prism': 'name',
        'Prism': 'Name',
        'Jeff Klukas': 'author',
        'jklukas@simple.com': 'email',
    }

    ignorables = IGNORABLES + [
        'target',
        '.ensime_cache',
    ]

    emptiables = [
        'banner.txt'
    ]

    petrify('prism_original', 'service_skeleton', replacements, ignorables)

    replacements = {
        'name': 'spoo',
        'Name': 'Spoo',
        'author': 'Keldor Skeletor',
        'email': 'keldor@skeletor.net',
    }

    rehydrate('service_skeleton', 'spoo', replacements)

if __name__ == "__main__":
    main()
