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

# This GDrive class is based on a sample file provided by Google

import logging
import uuid

import apiclient
import markdown

import sanitizer
import bookfile

log = logging.getLogger(__name__)

# TODO: Implement this
class FileStorage():
	pass

class GDriveFileProcessorFactory(FileStorage):
	def get_processor(self, dfile):
		font_mime_type_list = [
			"application/font-woff",
			"application/font-otf",
			"application/x-font-ttf",
			"application/x-font-opentype",
			"application/font-sfnt"
		]
		mime_type = dfile['mimeType']

		log.debug("File name: %s, mime type: %s" % (dfile.get('title'), mime_type))

		if mime_type == "application/vnd.google-apps.document":
			return GDriveDocProcessor()
		elif mime_type == "text/x-markdown":
			return GDriveMDProcessor()
		elif mime_type.startswith("image/"):
			return GDriveImageProcessor()
		elif mime_type == "text/css":
			return GDriveStyleProcessor()
		elif mime_type in font_mime_type_list:
			return GDriveFontProcessor()
		elif mime_type in ["application/xml", "text/xml"]:
			return GDriveFileProcessor()
		elif mime_type == "application/vnd.google-apps.spreadsheet":
			return GDriveSpreadProcessor()
		elif mime_type in ["application/xhtml+xml", "text/html"]:
			return GDriveXHTMLProcessor()
		else:
			log.warning("Unknown mime type: %s (file: %s)" % (mime_type, dfile.get('title')))
			return GDriveFileProcessor()

def GDriveDownloader(service, download_url):
	if download_url:
		resp, content = service._http.request(download_url)
		if resp.status == 200:
			log.debug("Downloader: Status: %s" % resp)
			return content
		else:
			log.error("Downloader: An error occurred: %s" % resp)
			return None
	else:
		# The file doesn't have any content stored on Drive.
		return None


class GDriveFileProcessor(object):
	def process(self, service, dfile):
		content = self.download(service, dfile)
		filename = dfile.get('title').replace(" ", "")
		return bookfile.BookFileUnknown(filename, content, folder=None, fmime=dfile['mimeType'])

	def download(self, service, dfile):
		download_url = dfile.get('downloadUrl')
		return GDriveDownloader(service, download_url)

class GDriveImageProcessor(GDriveFileProcessor):
	def process(self, service, dfile):
		content = self.download(service, dfile)
		filename = dfile.get('title').replace(" ", "")
		return bookfile.BookFileImage(filename, content, dfile['mimeType'])

class GDriveFontProcessor(GDriveFileProcessor):
	def process(self, service, dfile):
		content = self.download(service, dfile)
		filename = dfile.get('title').replace(" ", "")
		return bookfile.BookFileFont(filename, content, dfile['mimeType'])

class GDriveStyleProcessor(GDriveFileProcessor):
	def process(self, service, dfile):
		content = self.download(service, dfile)
		filename = dfile.get('title').replace(" ", "")
		return bookfile.BookFileStyle(filename, content)

class GDriveXHTMLProcessor(GDriveFileProcessor):
	def process(self, service, dfile):
		content = self.download(service, dfile)
		filename = dfile.get('title').replace(" ", "")
		return bookfile.BookFileUnknown(filename, content, folder="Text", fmime="application/xhtml+xml")

class GDriveDocProcessor(GDriveFileProcessor):
	def process(self, service, dfile):
		html_content = self.download(service, dfile)
		sanitzr = sanitizer.Sanitizer()
		html_content = sanitzr.sanitize(html_content)
		filename = "text__" + dfile.get('title').replace(" ", "") + "_" + unicode(uuid.uuid4()) + ".html"

		return bookfile.BookFileText(filename, html_content)

	def download(self, service, dfile):
		download_url = dfile['exportLinks']['text/html']
		return GDriveDownloader(service, download_url)

class GDriveMDProcessor(GDriveFileProcessor):
	def process(self, service, dfile):
		md_content = self.download(service, dfile)
		xml_content = markdown.markdown(md_content.decode("utf8"), extensions=['extra'])
		html_content = sanitizer.wrap_content(xml_content)
		filename = "text__" + dfile.get('title').replace(" ", "") + "_" + unicode(uuid.uuid4()) + ".html"
		return bookfile.BookFileText(filename, html_content)

class GDriveSpreadProcessor(GDriveFileProcessor):
	def process(self, service, dfile):
		csv_content = self.download(service, dfile)	
		filename = dfile.get('title')
		return bookfile.BookFileUnknown(filename, csv_content, folder=None, fmime=None)

	def download(self, service, dfile):
		pdf_url = dfile['exportLinks']['application/pdf']
		csv_url = pdf_url[:len(pdf_url)-3] + "csv"
		return GDriveDownloader(service, csv_url)


class GDrive(FileStorage):
	def __init__(self, cache=False):
		self.cache = cache
		self.authorize()
	
	def authorize(self):
		import httplib2
		import pprint

		from apiclient.discovery import build
		from oauth2client.client import OAuth2WebServerFlow
		from oauth2client.file import Storage

		# Copy your credentials from the APIs Console (https://code.google.com/apis/console/)
		CLIENT_ID = '447065192799-5uofsvr635rm62fpt5nncj69g60rglf1.apps.googleusercontent.com'
		CLIENT_SECRET = '9KoSX3kpNPFUY4TV4rXZgZjD'

		# Check https://developers.google.com/drive/scopes for all available scopes
		OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

		# Redirect URI for installed apps
		REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
		#REDIRECT_URI = 'http://localhost:8000'

		authorized = False
		if self.cache:
			# Path to the crendentials
			CRED_FILENAME = 'credentials'

			### For storing token
			storage = Storage(CRED_FILENAME)

			if storage.get():
				credentials = storage.get()
				authorized = True

		if (not self.cache) or (not authorized):
			# Run through the OAuth flow and retrieve authorization code
			flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
			authorize_url = flow.step1_get_authorize_url()
			print "=========AUTHORIZATION=============="
			print 'Go to the following link in your browser:\n' + authorize_url
			print "===================================="
			code = raw_input('Enter verification code: ').strip()
			credentials = flow.step2_exchange(code)

			### Storing access token and a refresh token in CRED_FILENAME
			if self.cache:
				storage.put(credentials)

		# Create an httplib2.Http object and authorize it with our credentials
		http = httplib2.Http()
		http = credentials.authorize(http)

		self.service = build('drive', 'v2', http=http)

	# TODO: Implement
	def verify_folder(self, service, folder_id):
		# Does the folder exist?
		pass


	def retrieve_all_files(self):
		from apiclient import errors
		result = []
		page_token = None
		while True:
			try:
				param = {}
				if page_token:
					param['pageToken'] = page_token
				files = self.service.files().list(**param).execute()

				result.extend(files['items'])
				page_token = files.get('nextPageToken')
				if not page_token:
					break
			except errors.HttpError, error:
				log.error("An error occurred: %s" % error)
				break
		return result

	def get_file_list(self, folder_id):
		from apiclient import errors
		file_ids = []
		page_token = None
		while True:
			try:
				param = {"q": "trashed=false and mimeType != 'application/vnd.google-apps.folder'"}
				if page_token:
					param['pageToken'] = page_token

				children = self.service.children().list(
								folderId=folder_id, **param).execute()

				for child in children.get('items', []):
					file_ids.append(child['id'])

				page_token = children.get('nextPageToken')

				if not page_token:
					break

			except errors.HttpError, error:
				log.error("An error occurred: %s" % error)
				break
		
		return file_ids

	def get_file_metadata(self, file_id):
		return self.service.files().get(fileId=file_id).execute()


	def print_file_metadata(self, log, file_id, prefix="\t"):
		from apiclient import errors
		try:
			_file = self.get_file_metadata(file_id)

			log.info("{}Title: {}".format(prefix, _file["title"].encode("utf8")))
			log.info("{}MIME type:: {}".format(prefix, _file["mimeType"].encode("utf8")))
		except errors.HttpError, error:
			log.error("An error occurred: %s" % error)


if __name__ == '__main__':
	drive = GDrive()
	file_ids = drive.get_file_list("0B--lHppejR64bXBJZ3YwT0tJM00")

	print 'Number of files: %s' % len(file_ids)
	
	for id in file_ids:
		drive.download_file(id)

