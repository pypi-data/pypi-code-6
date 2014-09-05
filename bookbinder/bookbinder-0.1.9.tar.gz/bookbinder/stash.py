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


import os
import tempfile
import itertools
import logging
import re
import uuid   #needed for embedding images
import urllib #needed for embedding images

from bs4 import BeautifulSoup

import metadata
import epub
import toc
import bookfile  #needed for embedding images


log = logging.getLogger(__name__)

class Stash(object):
	def __init__(self, base, epub_name):
		self.base = base
		self.epub_name = epub_name

		self.text_queue = []
		self.data_queue = []

		self.process_queue = []
		self.content_queue = []

		# Lists is only used for printing debug info
		self.lists = {
				"Text": self.text_queue,
				"Data": self.data_queue
			}

		self.metadata = metadata.Metadata()

	def mkdirs(self):
		import os, errno

		dir_list = ["META-INF", "OEBPS", "OEBPS/Fonts", "OEBPS/Images", "OEBPS/Styles", "OEBPS/Text"]

		for d in dir_list:
			path =  os.path.join(self.base, d)
			log.debug("Creating directory: %s" % path)

			try:
				os.makedirs(path)
			except OSError as exc:
				if exc.errno == errno.EEXIST and os.path.isdir(path):
					pass
				else:
					raise

	#TODO: Does this really belong here?
	def mark_footnotes(self, bf):
		soup = BeautifulSoup(bf.fcontent)
		body = soup.body

		log.debug("Looking for footnotes: {}".format(bf.fname.encode("utf8")))

		for div in body.find_all("div"):
			for a in div.find_all("a"):
				if a.get("href", "").startswith("#ftnt_"):
					log.debug("Found footnote.")
					div['class'] = div.get("class", []) + ["footnote"]

		soup.body.replace_with(body)
		return str(soup)

	#TODO: Does this really belong here?
	def embed_images(self, bf):
		soup = BeautifulSoup(bf.fcontent)
		body = soup.body

		log.debug("Looking for images: {}".format(bf.fname.encode("utf8")))
		for img in body.find_all("img"):
			log.debug("Image found: {}".format(img.get("alt", "").encode("utf8")))
			log.debug("Image source: {}".format(img.get("src", "").encode("utf8")))
			img_name, img_extension = os.path.splitext(img.get("alt", ""))
			img_name = str(uuid.uuid4()) + img_extension
			log.debug("New image name: {}".format(img_name.encode("utf8")))
			img_content = urllib.urlopen(img.get("src", "")).read()

			img_fmime = ""

			if img_extension.lower() in [".png"]:
				img_fmime = "image/png"
			elif img_extension.lower() in [".gif"]:
				img_fmime = "image/gif"
			elif img_extension.lower() in [".jpg", ".jpeg"]:
				img_fmime = "image/jpeg"
			else:
				log.debug("Unknown file type: {}".format(img_extension.encode("utf8")))
				return

			img_file = bookfile.BookFileImage(img_name, img_content, img_fmime)

			img_file.enqueue(self)

			img["src"] = "../Images/" + img_name
			del img["alt"]
			del img["title"]

		soup.body.replace_with(body)
		return str(soup)

	def prepare_content_files(self):
		"""
		Sort and rename the content files
		"""
		log.info("Preparing content files...")
		self.text_queue = sorted(self.text_queue, key = lambda x : x.fname)

		counter = 1
		for bf in self.text_queue:
			bf.fcontent = self.embed_images(bf)
			bf.fcontent = self.mark_footnotes(bf)
			log.debug("Renaming {}".format(bf.fname.encode("utf8")))
			bf.fname = "Section%04d.xhtml" % counter
			counter = counter + 1

	def store_files_to_disk(self):
		"""
		Store content files to disk and add all files to
		either the content queue or the process queue
		for further processing.
		"""
		for bf in itertools.chain(self.text_queue, self.data_queue):
			if bf.folder == None:
				# Not a typical content file, needs further processing
				log.debug("Data file: %s" % bf.fname)
				self.process_queue.append(bf)
			else:
				filepath =  os.path.join(self.base, "OEBPS", bf.folder, bf.fname)
				log.debug("Exporting: %s" % filepath)

				with open(filepath, "w") as f:
					f.write(bf.fcontent)
				self.content_queue.append(bf)

		self.content_queue = sorted(self.content_queue, key=lambda bf : bf.fname.lower())

	def process_remaining_files(self):
		"""
		Process the non-content files (e.g., metadata)
		"""
		log.info("Processing data files...")
		for f in self.process_queue:
			if f.fname == "metadata":
				log.info("Processing metadata...")
				with open("temp.csv", "w") as tf:
					tf.write(f.fcontent)
				self.metadata.extract_from_csv("temp.csv")
				os.remove("temp.csv")
			else:
				log.warning("File not processed: %s, mime type: %s" % (f.fname, f.mimetype))

	def update_book_metadata(self, book):
		book.set_title(self.metadata.first_title)

		for name, value, role, file_as, event, scheme in self.metadata.meta_list:
			kwargs = {}
			if role != "":
				kwargs["role"] = role
			if file_as != "":
				kwargs["file-as"] = file_as
			if event != "":
				kwargs["event"] = event
			if scheme != "":
				kwargs["scheme"] = scheme

			book.add_meta(name, value, **kwargs)
			
	def append_head_tags(self, soup, style_list):
		log.debug("Generating the stylesheet link tags...")
		styles = sorted(style_list, key = lambda x : x.id)

		style_tag = ""
		for item in styles:
			style_tag = style_tag + """<link href="../%s" rel="stylesheet" type="text/css"/>\n""" % item.path

		links = BeautifulSoup(style_tag)
		
		log.debug("Generating the new <title> tag...")
		new_title = soup.new_tag("title")
		new_title.string = self.metadata.first_title
		
		soup.head.append(links)
		if soup.title:
			soup.title.replace_with(new_title)
		else:
			soup.head.append(new_title)
		
		return soup
			
	def update_html_tags(self, toc_list, style_list):
		log.debug("Going through the content files for tag update...")
		
		for item in toc_list:
			#TODO: Refactor
			with open(os.path.join(self.base, "OEBPS", item.path), "r") as f:
				soup = BeautifulSoup(f)

				if soup.html:
					if soup.head == None:
						log.warning("No <head> tag in HTML, creating one. File: %s" % item.path)
						head_tag = soup.new_tag("head")
						soup.html.insert(0, head_tag)
					
					log.debug("Linking stylesheet(s) and updating <title> tags. File: %s" % item.path)
					soup = self.append_head_tags(soup, style_list)
				else:
					log.error("HTML file doesn't contain the <html> tag. Stylesheet(s) cannot be added. File: %s" % item.path)
					
			with open(os.path.join(self.base, "OEBPS", item.path), "w") as f:
				f.write(unicode(soup).encode("utf8"))

	
	def generate_toc(self, book, toc_list):
		root = toc.TocNode(0, 0, "", "")
		
		log.info("Generating table of contents...")
		playorder = 1
		for item in toc_list:
			path = os.path.join(self.base, "OEBPS", item.path)
			source_path = re.compile('^.*/OEBPS/').sub('', path)
			with open(path, "r") as f:
				soup = BeautifulSoup(f)
				for header in soup.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
					depth = int(float(header.name[1:]))
					log.debug("Heading found (depth: {}): {}".format(str(depth), header))
					try:
						source = source_path + "#" + header["id"].decode("utf8")
					except:
						log.debug("Heading doesn't have an ID. Creating one...")
						header["id"] = u"bbheading-" + unicode(playorder)
						source = source_path + "#" + header["id"]
						log.debug("New heading: {}".format(header.encode("utf8")))

					text = header.text
					node = toc.TocNode(depth, playorder, text, source)
					root.add_child(node)
					playorder = playorder + 1

			#TODO opening the file twice
			with open(path, "w") as f:
				f.write(unicode(soup).encode("utf8"))
		
		log.debug("Table of contents generation complete...")
		log.debug("TOC depth: {}".format(root.maxlevel))
		book.set_toc_root(root)

	def generate_epub(self):
		import shutil

		book = epub.EpubBook()

		self.update_book_metadata(book)

		toc_list = []
		style_list = []

		for bf in self.content_queue:
			item = book.add_item(bf)
			
			if item.path.startswith("Text"):
				book.add_spine_item(item)
				toc_list.append(item)
			elif item.path.startswith("Styles"):
				style_list.append(item)
				
		self.update_html_tags(toc_list, style_list)

		self.generate_toc(book, toc_list)

		book.create_book(self.base)
		epub_file_path = os.path.join(os.getcwd(), self.epub_name + ".epub")
		epub.EpubBook.create_archive(self.base, epub_file_path)

		shutil.rmtree(self.base)

		return epub_file_path

	def export(self):
		log.debug("Exporting stash...")
		self.mkdirs()
		self.prepare_content_files()
		self.store_files_to_disk()
		self.process_remaining_files()

		epub_file_path = self.generate_epub()

		return epub_file_path

	def __str__(self):
		str = "Stash content:\n"
		for k, l in self.lists.iteritems():
			str = str + "\t" + k + ":\n"
			for book in l:
				str = str + "\t\t" + book.__str__() + "\n"

		return str


