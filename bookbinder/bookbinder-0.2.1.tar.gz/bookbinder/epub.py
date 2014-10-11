# -*- coding: utf-8 -*-

"""
Copyright (c) 2012, Bin Tan
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

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


# This source file is based on Bin Tan's python-epub-builder
# located at https://code.google.com/p/python-epub-builder/
# The code is heavily modified

import itertools
import os
import shutil
import subprocess
import uuid
import zipfile
import re
from genshi.template import TemplateLoader
import logging

import templates

log = logging.getLogger(__name__)

class EpubItem:
	def __init__(self):
		self.id = u""
		self.path = u""
		self.mime_type = u""

class EpubBook:
	def __init__(self):
		self.loader = TemplateLoader(
								os.path.join(os.path.dirname(__file__), 'templates'),
								auto_reload=True
								)

		self.rootDir = u""
		self.uuid = uuid.uuid1()

		self.title = u""
		self.meta_info = []

		self.items = []

		self.cover_image = None
		self.title_page = None

		self.spine = []
		self.guide = {}

		self.toc_root = None

	def set_title(self, title):
		self.title = title
		
	def add_meta(self, metaName, metaValue, **metaAttrs):
		self.meta_info.append((unicode(metaName), unicode(metaValue), metaAttrs))
	
	def get_meta_tags(self):
		l = []
		for metaName, metaValue, metaAttr in self.meta_info:
			beginTag = '<dc:%s' % metaName
			if metaAttr:
				for attrName, attrValue in metaAttr.iteritems():
					beginTag += ' opf:%s="%s"' % (attrName, attrValue)
			beginTag += '>'
			endTag = '</dc:%s>' % metaName
			l.append((beginTag, metaValue, endTag))
		return l

	def get_all_items(self):
		return sorted(self.items, key = lambda x : x.id)

	def add_item(self, bookfile):
		item = EpubItem()
		item.id = re.sub(r'\W+', '_', unicode(bookfile.folder + "_" + bookfile.fname))
		item.path = unicode(bookfile.folder + "/" + bookfile.fname)
		item.mime_type = unicode(bookfile.mimetype)
		self.items.append(item)
		return item

	def set_toc_root(self, root):
		self.toc_root = root

	def get_spine(self):
		return sorted(self.spine)
	
	def add_spine_item(self, item, linear = True, order = None):
		if order == None:
			order = (max(order for order, _, _ in self.spine) if self.spine else 0) + 1
		self.spine.append((order, item, linear))

	def get_guide(self):
		return sorted(self.guide.values(), key = lambda x : x[2])

	def add_guide_item(self, href, title, type):
		assert type not in self.guide
		self.guide[type] = (href, title, type)

	def __write_container_XML(self):
		fout = open(os.path.join(self.rootDir, 'META-INF', 'container.xml'), 'w')
		fout.write(templates.container_xml)
		fout.close()

	def __write_toc_NCX(self):
		fout = open(os.path.join(self.rootDir, 'OEBPS', 'toc.ncx'), 'w')
		toc = templates.toc_ncx.format(book=self, navmap=self.toc_root.export_navmap())
		fout.write(toc.encode("utf8"))
		fout.close()
	
	def __write_content_OPF(self):
		fout = open(os.path.join(self.rootDir, 'OEBPS', 'content.opf'), 'w')
		tmpl = self.loader.load('content.opf')
		stream = tmpl.generate(book = self)
		fout.write(stream.render('xml').encode("utf8"))
		fout.close()

	def __write_mimetype(self):
		fout = open(os.path.join(self.rootDir, 'mimetype'), 'w')
		fout.write('application/epub+zip')
		fout.close()

	@staticmethod
	def __listManifestItems(contentOPFPath):
		from bs4 import BeautifulSoup
		
		items = []
		with open(contentOPFPath, "r") as f:
			soup = BeautifulSoup(f)
			for item in soup.find_all("opf:item"):
				items.append(item["href"])
		return items

	@staticmethod
	def create_archive(input_path, output_path):
		fout = zipfile.ZipFile(output_path, 'w')
		cwd = os.getcwd()
		os.chdir(input_path)
		fout.write('mimetype', compress_type = zipfile.ZIP_STORED)
		fileList = []
		fileList.append(os.path.join('META-INF', 'container.xml'))
		fileList.append(os.path.join('OEBPS', 'content.opf'))
		for itemPath in EpubBook.__listManifestItems(os.path.join('OEBPS', 'content.opf')):
				fileList.append(os.path.join('OEBPS', itemPath))

		for filePath in fileList:
			fout.write(filePath, compress_type = zipfile.ZIP_DEFLATED)
		fout.close()
		os.chdir(cwd)
	
	def create_book(self, rootDir):
		self.rootDir = rootDir
		self.__write_mimetype()
		self.__write_container_XML()
		self.__write_content_OPF()
		self.__write_toc_NCX()
