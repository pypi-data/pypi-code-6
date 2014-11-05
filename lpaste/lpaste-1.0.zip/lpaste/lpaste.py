#!/usr/bin/env python
from __future__ import absolute_import, print_function

import os
import sys
import re
import ConfigParser
import getpass
import urllib2
import importlib
from optparse import OptionParser
from textwrap import dedent

import pkg_resources
import webbrowser
import poster.streaminghttp
from poster.encode import multipart_encode

from . import keyring
from .source import Source

try:
	mod_name = 'lpaste.%s.clipboard' % sys.platform
	clipb = importlib.import_module(mod_name)
except ImportError:
	clipb = None

version = pkg_resources.require('lpaste')[0].version

BASE_HEADERS = {
	'User-Agent': 'lpaste ({version}) Python ({sys.version})'.format(**vars())
}

def install_opener(*handlers):
	opener = poster.streaminghttp.register_openers()
	map(opener.add_handler, handlers)

def get_options():
	"""
	$prog [options] [<file>]

	lpaste {version}

	If file is not supplied, stdin will be used.
	"""
	fileconf = ConfigParser.ConfigParser()
	fileconf.read('/etc/lpasterc')
	fileconf.read(os.path.expanduser('~/.lpasterc'))
	try:
		default_url = fileconf.get('lpaste', 'url')
	except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
		default_url = 'http://a.libpa.st/'
	try:
		file_user = fileconf.get('lpaste', 'user')
	except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
		file_user = ''

	default_user = (file_user or os.environ.get('QPASTEUSER')
		or os.environ.get('USERNAME') or getpass.getuser())

	parser = OptionParser(usage=dedent(get_options.__doc__.format(**globals())).lstrip())

	parser.add_option('-s', '--site', dest='site',
		default=default_url,
		help="URL for the library paste site to use. By default: %s" %
		default_url)
	parser.add_option('-t', '--format', dest='format', default='_',
		help="Which syntax code highlighter would you like to use? "
		"Defaults to plain text.")
	parser.add_option('-u', '--username', dest='username',
		default=default_user, help="Username to paste as, attempts to "
		"use system account name if none specified.")
	parser.add_option('-l', '--longurl', dest='longurl',
		action="store_true", default=False,
		help="Use a long url instead of the default short")
	parser.add_option('-a', '--attach', dest='attach',
		action="store_true", default=False,
		help="Upload the file as an attachment instead of as code/text")
	parser.add_option('-b', '--browser', dest='browser',
		action="store_true", default=False,
		help="Open your paste in a new browser window after it's "
		"uploaded")
	parser.add_option('-c', '--clipboard',
		action="store_true", default=False,
		help="Get the input from the clipboard")
	parser.add_option('--auth-username', default=default_user,
		help="The username to use when HTTP auth is required",)
	if not keyring.enabled:
		parser.add_option('--auth-password',
			help="The password to use when HTTP auth is required",)
	options, args = parser.parse_args()
	options.file = args.pop() if args else None
	if args:
		parser.error("At most one positional arg (file) is allowed.")
	if options.file and options.clipboard:
		parser.error("Either supply a file or --clipboard, but not both")
	if options.clipboard:
		if not clipb:
			parser.error("Clipboard support not available - you must "
				"supply a file")
		source = clipb.get_source()
	else:
		use_stdin = options.file in (None, '-')
		stream = open(options.file, 'rb') if not use_stdin else sys.stdin
		filename = os.path.basename(options.file) if not use_stdin else None
		if options.attach:
			source = Source.from_stream(stream, filename=filename)
		else:
			source = Source(code=stream.read())

	options.source = source
	if hasattr(source, 'format'):
		options.format = source.format
	return options


def main():

	options = get_options()

	paste_url = options.site
	data = {'nick': options.username, 'fmt': options.format, }
	if not options.longurl:
		data['makeshort'] = 'True'
	options.source.apply(data)
	datagen, headers = multipart_encode(data)
	headers.update(BASE_HEADERS)

	if keyring.enabled:
		auth_manager = keyring.FixedUserKeyringPasswordManager(options.auth_username)
	else:
		auth_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
		auth_manager.add_password(None, options.site,
			options.auth_username,
			options.auth_password or getpass.getpass())
	auth_handler = urllib2.HTTPBasicAuthHandler(auth_manager)
	install_opener(auth_handler)
	req = urllib2.Request(paste_url, datagen, headers)
	try:
		res = urllib2.urlopen(req)
	except urllib2.HTTPError as e:
		if e.getcode() == 401:
			print("Invalid username or password", file=sys.stderr)
			if keyring.enabled:
				realm = get_realm(e.hdrs['www-authenticate'])
				auth_manager.clear_password(realm, paste_url)
				print("Password cleared; Please try again.", file=sys.stderr)
			return
		if e.getcode() == 500:
			import pdb
			pdb.set_trace()
		raise
	url = res.geturl()
	if clipb: clipb.set_text(url)
	print('Paste URL:', url)
	if options.browser:
		print("Now opening browser...")
		webbrowser.open(url)

def get_realm(authenticate_header):
	pattern = re.compile('\w+ realm="(?P<realm>.*)"')
	res = pattern.match(authenticate_header)
	return res.groupdict()['realm']

if __name__ == '__main__':
	main()
