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


from bs4 import BeautifulSoup
import cssutils
import logging

from templates import content_template

log = logging.getLogger(__name__)

class Sanitizer:
	def sanitize(self, content):
		soup = BeautifulSoup(content)
		css = self.extract_css(soup)
		alltags, usables = self.find_usable_rules(css)
		clean_soup = self.clean(soup, alltags, usables)

		ret_soup = BeautifulSoup(content_template)
		ret_soup.body.replace_with(clean_soup.body)

		return unicode(ret_soup)

	def extract_css(self, soup):
		css_sheet = cssutils.css.CSSStyleSheet()

		for styletag in soup.find_all('style', type='text/css'):
			if not styletag.string: # probably an external sheet
				continue
			for rule in cssutils.parseString(styletag.string):
				css_sheet.add(rule)
		
		log.debug("Extracted embedded stylesheet:\n%s" % css_sheet.cssText)
		return css_sheet

	def find_usable_rules(self, sheet):
		"""Finds those CSS classes which will be used in the final HTMl file.
		These include the styles listed in the "usables" dictionary.
		"""
		usables = {
			"bolds": [],
			"italics": [],
			"blockquotes": [],
			"double_blockquotes": [],
			"triple_blockquotes": [],
			"underlines": [],
			"right_aligned": [],
			"centered": [],
			"strikethrus": [],
			"subscripts": [],
			"superscripts": [],
			"alltags": [],
		}

		alltags = []
		
		for rule in sheet:
			if (rule.type == rule.STYLE_RULE) and (rule.selectorText.startswith(".c")):
				alltags.append(rule.selectorText[1:])
				for property in rule.style:
					if property.name == "font-weight" and property.value == "bold":
							usables["bolds"].append(rule.selectorText[1:])
						
					if property.name == "font-style" and property.value == "italic":
							usables["italics"].append(rule.selectorText[1:])
							
					if property.name == "margin-left":
						if property.value == "36pt":
							usables["blockquotes"].append(rule.selectorText[1:])
						if property.value == "72pt":
							usables["double_blockquotes"].append(rule.selectorText[1:])
						if property.value == "108pt":
							usables["double_blockquotes"].append(rule.selectorText[1:])
				
					if property.name == "text-align":
						if property.value == "center":
							usables["centered"].append(rule.selectorText[1:])
						if property.value == "right":
							usables["right_aligned"].append(rule.selectorText[1:])
							
					if property.name == "text-decoration":
						if property.value == "line-through":
							usables["strikethrus"].append(rule.selectorText[1:])
						if property.value == "underline":
							usables["underlines"].append(rule.selectorText[1:])

					if property.name == "vertical-align":
						if property.value == "super":
							usables["superscripts"].append(rule.selectorText[1:])
						if property.value == "sub":
							usables["subscripts"].append(rule.selectorText[1:])

		return (alltags, usables)

	def remove_class_from_tag(self, tag, cl):
		tag.get('class').remove(cl)
		if (len(tag.get('class'))) < 1:
			del tag["class"]

		return tag


	def tagify(self, class_list, soup, ntag):
		body = soup.body
		for cl in class_list:
			for tag in body.find_all(class_=cl):
				tag.wrap(soup.new_tag(ntag))
				tag = self.remove_class_from_tag(tag, cl)
		
		
	def remove_unused_classes(self, soup, alltags, usables):
		body = soup.body

		log.debug("Removing all class attributes except for the <span> and <p> tags.")
		for tag in soup.find_all():
			if tag.name.lower() not in ["span", "p"]:
				if tag.has_attr('class'):
					del tag["class"]

		all_usables = []
		for v in usables.itervalues():
			all_usables = all_usables + v

		for class_tag in alltags:
			if class_tag not in all_usables:
				for tag in body.find_all(class_=class_tag):
					tag = self.remove_class_from_tag(tag, class_tag)

		return soup
				
	def clean(self, in_soup, alltags, usables):
		soup = self.remove_unused_classes(in_soup, alltags, usables)

		self.tagify(usables["bolds"], soup, "strong")
		self.tagify(usables["italics"], soup, "em")
		self.tagify(usables["subscripts"], soup, "sub")
		self.tagify(usables["superscripts"], soup, "sup")
		self.tagify(usables["blockquotes"], soup, "blockquote")

		body = soup.body
		del body["class"]

		for cl in usables["double_blockquotes"]:
			for tag in body.find_all(class_=cl):
				tag.wrap(soup.new_tag("blockquote"))
				tag.wrap(soup.new_tag("blockquote"))
				tag = self.remove_class_from_tag(tag, cl)
		#TODO: This doesn't seem to work
		for cl in usables["triple_blockquotes"]:
			for tag in body.find_all(class_=cl):
				tag.wrap(soup.new_tag("blockquote"))
				tag.wrap(soup.new_tag("blockquote"))
				tag.wrap(soup.new_tag("blockquote"))
				tag = self.remove_class_from_tag(tag, cl)

		for cl in usables["underlines"]:
			for tag in body.find_all(class_=cl):
				tag["class"] = "underlined"

		for cl in usables["right_aligned"]:
			for tag in body.find_all(class_=cl):
				tag["class"] = "right-aligned"

		for cl in usables["centered"]:
			for tag in body.find_all(class_=cl):
				tag["class"] = "center-aligned"

		for cl in usables["strikethrus"]:
			for tag in body.find_all(class_=cl):
				tag["class"] = "strike-through"

		for tag in body.find_all("span"):
			if tag.get('class') == None:
				tag.unwrap()

		# Used for the footnotes
		"""
		for tag in body.find_all("div"):
			if tag.get('class') == None:
				tag.unwrap()
		"""
		
		for tag in body.find_all("a"):
			if tag.text == "":
				tag.unwrap()

		return soup

def wrap_content(content):
	soup = BeautifulSoup(content)

	ret_soup = BeautifulSoup(content_template)
	ret_soup.body.append(soup)

	return unicode(ret_soup)

if __name__ == '__main__':
	with open("test-data/TestDoc.html") as f:
		sanitizer = Sanitizer()
		content = f.read()
		content = sanitizer.sanitize(content)

		with open("outfile.html", "w") as f:
			f.write(content.encode('utf8'))
