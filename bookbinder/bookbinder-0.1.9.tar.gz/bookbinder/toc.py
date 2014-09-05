#!/usr/bin/python
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------
# Copyright (c) 2014 Eren Inan Canpolat
# Author: Eren Inan Canpolat <eren.canpolat@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------

import logging

log = logging.getLogger(__name__)

class TocNode(object):
	def __init__(self, level, playorder, text, source, empty=False):
		self.playorder = playorder
		self.text = text
		self.source = source
		self.level = level
		self.children = []
		self.parent = None
		self.maxlevel = 0
		self.empty = empty
		
	def add_child(self, child):
		if child.level == self.level + 1:
			self.children.append(child)
			child.parent = self
			
		elif len(self.children) > 0:
			level = self.children[-1].add_child(child)
			
		else:
			log.warning("There is a jump in document heading structure: {}".format(child.text.encode("utf8")))
			empty_child = TocNode(self.level + 1, self.playorder + 1, "", child.source, empty=True)
			self.children.append(empty_child)
			empty_child.add_child(child)
			
		if child.level > self.maxlevel:
			self.maxlevel = child.level

	def __str__(self):
		print "\t"*self.level + self.text
		for child in self.children:
			child.__str__()

	def export_navmap(self):
		navmap = u"<navMap>\n"
		
		for child in self.children:
			navmap = navmap + child.export_navpoint()
			
		navmap = navmap + u"</navMap>"
		
		return navmap

	def export_navpoint(self):
		navpoint = u""
		first_indent = u"  "*self.level
		second_indent = first_indent + "  "
		if self.empty == False:
			navpoint = first_indent + u'<navPoint id="navPoint-{}" playOrder="{}">\n'.format(self.playorder, self.playorder)
			navpoint = navpoint + second_indent + u'<navLabel><text>{}</text></navLabel>\n'.format(self.text)
			navpoint = navpoint + second_indent + u'<content src="{}"/>\n'.format(self.source)
		if len(self.children) > 0:
			for child in self.children:
				navpoint = navpoint + child.export_navpoint()
		if self.empty == False:
			navpoint = navpoint + first_indent + u'</navPoint>\n'
		
		return navpoint

