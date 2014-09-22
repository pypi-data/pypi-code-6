#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Binh Vu <binh@toan2.com>"

"""

	Execute some of after initialization module

"""
class PostProcess(object):

	def __init__(self, module):
		self.module = module

	def execute(self, config, extra):
		if "postexecute" in config:
			module = {
				"location": self.module.location,
				"name": config["name"],
				"root": extra["root"]
			}

			exec(config["postexecute"])