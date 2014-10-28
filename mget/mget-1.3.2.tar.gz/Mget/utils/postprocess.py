#!/usr/bin/env python3

class PostProcess:
	def __init__ (self, plist = []):
		self.process_list = plist

	def addProcess (self, process):
		self.process_list = process

	def run (self):
		for process in self.process_list:
			print(process)
