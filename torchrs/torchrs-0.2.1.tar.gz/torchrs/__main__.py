#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Binh Vu <binh@toan2.com>"

import os, sys

from .resolver import Resolver

if __name__ == "__main__":
	composerPath = os.path.join(os.path.abspath("."), "composer.json")

	if not os.path.exists(composerPath):
		print "composer.json not found"
		exit(0)

	if sys.argv[1] == "install":
		resolver = Resolver(composerPath)
		resolver.resolve()
	else:
		print "not support yet"
