#!/usr/bin/env python3
"""pysnipp

Usage:
    pysnipp add <category> <name>
    pysnipp show <category> <name>
    pysnipp edit <category> <name>
    pysnipp rename <category> <name> <new-name>
    pysnipp delete <category> <name>
    pysnipp list [<searchstring>] [-C]
    pysnipp about

Options:
    -h, --help      :   show this help message
    add             :   add a snippet(need to supply category and name)
    edit            :   edit an existing snippet
    rename          :   rename your snippet name
    delete          :   delete a snippet
    list [-C]           :   list all snippets with content(or only a category)
    list            :   list all snippets(or only a category)
    about           :   show some information about pysnipp
"""
from .snippet import Snippet
from .controller import *
from docopt import docopt

__version__ = "0.5.1"

def main():
    arguments = docopt(__doc__)
    if arguments['add']:
        new = Snippet(arguments['<category>'], arguments['<name>'], '')
        if new.exists():
            new.content = new.get()
        else:
            new.commit()
        new.edit()

    elif arguments['show']:
        existing = Snippet(arguments['<category>'], arguments['<name>'])
        print(existing.get()),

    elif arguments['edit']:
        existing = Snippet(arguments['<category>'], arguments['<name>'])
        existing.edit()

    elif arguments['delete']:
        existing = Snippet(arguments['<category>'], arguments['<name>'])
        existing.delete()

    elif arguments['list']:
        if arguments["-C"]:
            if arguments['<searchstring>']:
                list_snippets_w_content(arguments['<searchstring>'])
            else:
                list_snippets_w_content()
        else:
           if arguments['<searchstring>']:
                list_snippets(arguments['<searchstring>'])
           else:
                list_snippets()

    elif arguments['rename']:
        existing = Snippet(arguments['<category>'], arguments['<name>'])
        existing.rename(arguments['<new-name>'])


    elif arguments['about']:
        print("""
        \033[92m
         ____        ____        _
        |  _ \ _   _/ ___| _ __ (_)_ __  _ __
        | |_) | | | \___ \| '_ \| | '_ \| '_ \\
        |  __/| |_| |___) | | | | | |_) | |_) |
        |_|    \__, |____/|_| |_|_| .__/| .__/
               |___/              |_|   |_|
        \033[0m                                 v%s

        PySnipp is a console based snippet manager written by Daniel Hauck
        for issues or bugs please write to pysnipp@hauck.it

        For more information go to http://hauck-daniel.de/pysnipp
        """ % __version__),
