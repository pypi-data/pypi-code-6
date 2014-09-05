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

import sys
import tempfile
import logging

import gdrive
import stash

log = logging.getLogger("bookbinder.main")

import pkg_resources
version = pkg_resources.require("bookbinder")[0].version

def init_logging():
	logging.basicConfig(level=logging.DEBUG,
				format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
				datefmt='%m-%d %H:%M',
				filename='bookbinder.log',
				filemode='w')

	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)-24s: %(levelname)-8s %(message)s')
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)

	apiclient_log = logging.getLogger("apiclient")
	apiclient_log.setLevel(logging.WARNING)

	oauth2client_log = logging.getLogger("oauth2client")
	oauth2client_log.setLevel(logging.WARNING)


def dry_run(folders, cache=False):
	drive = gdrive.GDrive(cache)

	log.info("================================")
	log.info("=============DRY RUN============")
	log.info("================================")

	for folderId in folders:
		if folderId == None:
			continue
		log.info("Processing folder: %s" % str(folderId))
		file_ids = drive.get_file_list(folderId)

		log.info("Number of files in the folder: %s" % str(len(file_ids)))

		count = 1
		for fid in file_ids:
			log.info("{:02d} - File ID: {}".format(count, fid))
			drive.print_file_metadata(log, fid, prefix="\t\t")
			count = count + 1

	log.info("=======DRY RUN COMPLETE=========")
	log.info("================================")

def process(folders, cache=False):
	drive = gdrive.GDrive(cache)
	dirpath = tempfile.mkdtemp()
	if len(folders) > 0:
		stash_ = stash.Stash(dirpath, folders[0])
	total_count = 0

	for folderId in folders:
		log.info("Processing folder: %s" % str(folderId))
		file_ids = drive.get_file_list(folderId)
		log.info("Number of files in the folder: %s" % str(len(file_ids)))

		if len(file_ids) > 0:
			total_count = total_count + len(file_ids)

			count = 0
			for fid in file_ids:
				log.debug("File ID: %s" % fid)
				log.debug("Retrieving file metadata...")
				dfile = drive.get_file_metadata(fid)
				processor = gdrive.GDriveFileProcessorFactory().get_processor(dfile)
				log.debug("Processing file...")
				bfile = processor.process(drive.service, dfile)
				bfile.enqueue(stash_)
				count = count + 1
			log.info("Number of files downloaded: %s" % count)

	if total_count > 0:
		epub_path = stash_.export()
		log.info("ePub ready at: %s" % epub_path)
	else:
		log.error("No files found. Please check the folder ID(s) you provided. If you don't know what a folder ID is, please see the user guide.")

def bindbook():
	import argparse

	init_logging()

	description= "ePub generation from Google Documents."
	parser = argparse.ArgumentParser(description=description)

	parser.add_argument("folders", nargs="+", help="ID(s) of the Google Drive folder(s) containing book content")
	parser.add_argument("-c", "--cache", action="store_true", help="cache credentials and use them for subsequent file access")
	parser.add_argument("-d", "--dryrun", action="store_true", help="list the files that would be processed for the book, but don't process them")
	parser.add_argument("-v", "--version", action="version", version="Book Binder version: {}".format(version))
	args = parser.parse_args()

	if args.dryrun:
		dry_run(args.folders, args.cache)
	else:
		process(args.folders, args.cache)


if __name__ == '__main__':
	bindbook()
