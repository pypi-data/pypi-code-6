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


class BookFile(object):
	def __init__(self, fname, fcontent, fmime):
		self.fname = fname
		self.fcontent = fcontent
		self.mimetype = fmime

	def enqueue(self, stash):
		stash.data_queue.append(self)

class BookFileText(BookFile):
	def __init__(self, fname, fcontent):
		self.folder = "Text"
		super(BookFileText, self).__init__(fname, fcontent.encode("utf8"), "application/xhtml+xml")

	def enqueue(self, stash):
		stash.text_queue.append(self)
		
class BookFileStyle(BookFile):
	def __init__(self, fname, fcontent):
		self.folder = "Styles"
		super(BookFileStyle, self).__init__(fname, fcontent, "text/css")

class BookFileImage(BookFile):
	def __init__(self, fname, fcontent, fmime):
		self.folder = "Images"
		super(BookFileImage, self).__init__(fname, fcontent, fmime)

class BookFileFont(BookFile):
	def __init__(self, fname, fcontent, fmime):
		self.folder = "Fonts"
		super(BookFileFont, self).__init__(fname, fcontent, fmime)

class BookFileUnknown(BookFile):
	def __init__(self, fname, fcontent, folder, fmime):
		self.folder = folder
		super(BookFileUnknown, self).__init__(fname, fcontent, fmime)
