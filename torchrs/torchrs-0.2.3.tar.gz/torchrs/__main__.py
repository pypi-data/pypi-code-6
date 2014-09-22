#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Binh Vu <binh@toan2.com>"

import os, sys

from .resolver import Resolver
from .shell.shell import Shell

def log(s):
	print s

if __name__ == "__main__":
	composerPath = os.path.join(os.path.abspath("."), "composer.json")

	if not os.path.exists(composerPath):
		print "composer.json not found"
		exit(0)

	if sys.argv[1] == "install":
		if len(sys.argv) > 2 and sys.argv[2] == "--hard":
			Shell.call(["rm", "__init__.py"], log)
			Shell.call(["rm", "-rf", "modules"], log)

		resolver = Resolver(composerPath)
		resolver.resolve()
	else:
		print "not support yet"
