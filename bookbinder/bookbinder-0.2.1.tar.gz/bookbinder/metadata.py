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

class Metadata(object):
	def __init__(self):
		self.first_title = "Untitled"
		self.meta_list = []

	def validate_metadata(self, name, role, file_as, event, scheme):
		from attributes import metadata_attributes, metadata_roles
		
		if name not in metadata_attributes.iterkeys():
			log.warning("Invalid metadata name: %s" % name)
			return False

		if role != "":
			if "role" not in metadata_attributes[name]:
				log.warning("Invalid metadata attribute: role")
				return False
			if role not in metadata_roles:
				log.warning("Invalid role attribute: %s" % role)
				return False
			
		if (file_as != "") and ("file-as" not in metadata_attributes[name]):
			log.warning("Invalid metadata attribute: file-as")
			return False

		if (event != "") and ("event" not in metadata_attributes[name]):
			log.warning("Invalid metadata attribute: event")
			return False

		if (scheme != "") and ("scheme" not in metadata_attributes[name]):
			log.warning("Invalid metadata attribute: scheme")
			return False
		
		log.debug("Metadata validation passed!")
		return True

	def extract_from_csv(self, _file):
		import csv
		
		log.debug("Parsing the CSV file...")
		with open(_file, 'rb') as f:
			reader = csv.reader(f)

			first_title_found = False
			for row in reader:
				log.debug(row)
				name = row[0].decode("utf-8")
				value = row[1].decode("utf-8")
				role = row[2].decode("utf-8")
				file_as = row[3].decode("utf-8")
				event = row[4].decode("utf-8")
				scheme = row[5].decode("utf-8")

				if name == "name":
					"""The first row may include headers"""
					continue

				if (not first_title_found) and (name == "title"):
					self.first_title = value
					first_title_found = True
				else:
					if self.validate_metadata(name, role, file_as, event, scheme):
						self.meta_list.append((name, value, role, file_as, event, scheme))

		self.meta_list.append(("contributor", "Book Binder", "bkp", "", "", ""))


if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
	logging.getLogger(__name__)
	
	Metadata().extract_from_csv("test-data/metadata.csv")
