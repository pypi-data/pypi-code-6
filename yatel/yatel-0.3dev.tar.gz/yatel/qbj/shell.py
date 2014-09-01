#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#==============================================================================
# DOCS
#==============================================================================

"""Interactive shell for QBJ

"""


#==============================================================================
# IMPORTS
#==============================================================================

import cmd
import json
import random

from yatel import db
from yatel.qbj import core


#==============================================================================
# CONSTANTS
#==============================================================================

PROMPT_0 = u"QBJ [{}]> "

PROMPT_1 = u"...\t"

PROMPT_2 = u"\t "


#==============================================================================
# CLASS
#==============================================================================

class QBJShell(cmd.Cmd):
    """Write your QBJQuery and end it with ';'

    Special Commands:

        - help: Print this help.
        - exec <PATH>: execute a query from a qbj file.
        - fhelp: Print a list of all available QBJ-functions
        - fhelp <FNAME>: print help about FNAME function.
        - indent <INT>: change indentation of response (Default: None).

    """

    def __init__(self, nw, debug):
        cmd.Cmd.__init__(self)

        nwdata = db.parse_uri(nw.uri)
        self.nw_name = "{}://***/{}".format(
            nwdata["engine"], nwdata["database"].rsplit("/", 1)[-1]
        )
        self.prompt_0 = PROMPT_0.format(self.nw_name)
        self.prompt = self.prompt_0
        self.intro  = "Yatel QBJ Console\n" + self.__doc__
        self.qbj = core.QBJEngine(nw)
        self.debug = debug
        self.indent = 2
        self.buff = []

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_EOF(self, args):
        """Exit on system end of file character"""
        print random.choice((
            "See you space cowboy", "The End", "Run Forrest, run!",
            "To be continued...", "I'll be back", "Hasta la vista baby",
            "This is not the end only the beginning"
        ))
        return self.do_exit(args)

    def do_fhelp(self, args):
        if args:
            cmd = u"""{
                "id": null,
                "function": {
                    "name": "help",
                    "kwargs": {
                        "fname": {"value": "%placeholder%", "type": "literal"}
                    }
                }
            };""".replace("%placeholder%", args)
        else:
            cmd = u"""{
                "id": null,
                "function": {"name": "help"}
            };"""
        self.default(cmd)

    def do_exec(self, fpath):
        """Excecute query from .qbj file"""
        with open(fpath) as fp:
            src = fp.read().strip()
            if not src.endswith(";"):
                src += ";"
            self.default(src)

    def do_help(self, args):
        print u"\t" + self.__doc__

    def do_indent(self, indent):
        try:
            if indent is None:
                self.indent = None
            else:
                self.indent = int(indent)
        except:
            self.indent = 2

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def default(self, line):
        """Execute a QBJ query
        """
        line = line.strip()
        self.buff.append(line)
        if line.endswith(";"):
            fullcmd = " ".join(self.buff)[:-1]
            self.buff = []
            if fullcmd.strip():
                try:
                    query = json.loads(fullcmd)
                    response = self.qbj.execute(query, self.debug)
                    print(
                        PROMPT_2 +
                        json.dumps(response, indent=self.indent)
                        + u"\n"
                    )
                except Exception as err:
                    print(PROMPT_2+unicode(err)+u"\n")
                finally:
                    self.prompt = self.prompt_0
            else:
                self.prompt = self.prompt_0
        else:
            self.prompt = PROMPT_1


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)


