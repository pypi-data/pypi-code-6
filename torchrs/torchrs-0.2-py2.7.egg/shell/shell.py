#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Binh Vu <binh@toan2.com>"

import subprocess

def func(line):
	pass

class Shell(object):

	@staticmethod
	def call(args, callback=func):
		process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		output = []
		for line in process.stdout:
			callback(line)
			output.append(line)
		process.wait()

		return output
