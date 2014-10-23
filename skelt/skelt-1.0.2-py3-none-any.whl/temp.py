#!/usr/bin/env python3

from skelt import petrify, rehydrate, IGNORABLES
from shutil import rmtree
from pathlib import Path

def main():

    target = Path('tempskel')
    if target.exists():
        rmtree(str(target))

    replacements = {
        # 'prism': 'name',
        # 'Prism': 'Name',
        # 'Jeff Klukas': 'author',
        # 'jklukas@simple.com': 'email',
        # 'Simple Finance Technology Corp.': 'company',
        # 'simple': 'domain'
        'scalafoo': 'name',
        'Scalafoo': 'Name',
        'Jeff Klukas': 'author',
        'jeff@klukas.net': 'email',
    }

    ignorables = IGNORABLES + [
        'target',
        '.ensime_cache',
    ]

    emptiables = [
        'banner.txt'
    ]

    petrify('scalafoo', 'tempskel', replacements, ignorables)

    # replacements = {
    #     'name': 'scalafoo',
    #     'Name': 'Scalafoo',
    #     'author': 'Jeff Klukas',
    #     'email': 'jeff@klukas.net',
    #     'company': 'ExampleCo',
    #     'domain': 'example',
    # }

    # rehydrate('tempskel', 'scalafoo', replacements)

if __name__ == "__main__":
    main()
