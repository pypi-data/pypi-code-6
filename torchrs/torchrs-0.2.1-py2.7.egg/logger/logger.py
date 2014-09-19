#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Binh Vu <binh@toan2.com>"

import sys

class Logger(object):

	TRACE = 0
	DEBUG = 1
	INFO  = 2
	ERROR = 3
	FATAL = 4

	def __init__(self, namespace, formatString="", level=INFO):
		self.namespace = namespace

		if formatString == "":
			self.formatString = "[{0}] - [{1}]\t- {2}"
		else:
			self.formatString = formatString

		# TRACE, DEBUG, INFO, ERROR, FATAL
		self.level = level

	def fatal(self, content):
		if self.level <= Logger.FATAL:
			self.log("FATAL", content)

	def error(self, content):
		if self.level <= Logger.ERROR:
			self.log("ERROR", content)

	def info(self, content):
		if self.level <= Logger.INFO:
			self.log("INFO", content)

	def debug(self, content):
		if self.level <= Logger.DEBUG:
			self.log("DEBUG", content)

	def trace(self, content):
		if self.level <= Logger.TRACE:
			self.log("TRACE", content)

	def log(self, tag, content):
		print self.formatString.format(self.namespace, tag, content)
		sys.stdout.flush()