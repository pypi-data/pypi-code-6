# -*- coding: utf-8 -*-
from __future__ import (division, print_function, unicode_literals)
#############################################################################
# Author  : Jerome ODIER, Jerome FULACHIER, Fabian LAMBERT, Solveig ALBRAND
#
# Email   : jerome.odier@lpsc.in2p3.fr
#           jerome.fulachier@lpsc.in2p3.fr
#           fabian.lambert@lpsc.in2p3.fr
#           solveig.albrand@lpsc.in2p3.fr
#
# Version : 1.X.X (2014)
#
#############################################################################

import os, sys, fuse, stat, errno, getpass, amifs.entry, pyAMI.client, pyAMI.config, pyAMI.exception

#############################################################################

fuse.fuse_python_api = (0, 2)

#############################################################################

class FS(fuse.Fuse):
	#####################################################################

	FSE = sys.getfilesystemencoding()

	#####################################################################

	def __init__(self, endpoint, *args, **kw):
		super(FS, self).__init__(*args, **kw)

		#############################################################
		# CREATE pyAMI CLIENT                                       #
		#############################################################

		self.client = pyAMI.client.Client(endpoint)

		#############################################################
		# CREATE ENTRY DIRECTORY                                    #
		#############################################################

		self.root = amifs.entry.Entry(self, None, amifs.entry.TYPE_DIR, '')

		#############################################################
		# CREATE `/version.txt`                                     #
		#############################################################

		self.root.new_reg(self, 'version.txt').data = pyAMI.config.version + '\n'

		#############################################################
		# CREATE `/authors.txt`                                     #
		#############################################################

		self.root.new_reg(self, 'authors.txt').data = pyAMI.config.authors + '\n'

		#############################################################
		# CREATE `/.htaccess`                                        #
		#############################################################

		self.root.new_reg(self, '.htaccess').data = 'Options +Indexes\n'

		#############################################################
		# CREATE `/command`                                         #
		#############################################################

		def __op(path, buff):
			self.root.new_reg(self, 'command_%s' % getpass.getuser()).data = '::command::%s' % buff

			return 0

		self.root.new_reg(self, 'command.magic', mode = 0o222).data = __op

	#####################################################################

	def getattr(self, path):
		#############################################################
		# LOOKUP PATH                                               #
		#############################################################

		file = self.root.lookup(path)

		if file is None:
			return -errno.ENOENT

		#############################################################
		# EXECUTE DEFERRED COMMAND                                  #
		#############################################################

		try:

			if file.data.startswith('::command::'):

				try:
					file.data = self.client.execute(file.data[11: ], format = 'csv')

				except pyAMI.exception.Error as e:
					file.data = e.__str__()

					print(e)

		except Exception:
			pass

		#############################################################
		# GET STAT                                                  #
		#############################################################

		return file.stat

	#####################################################################

	def readdir(self, path, offset):
		#############################################################
		# DEFAULT                                                   #
		#############################################################

		entries = ['.', '..']

		#############################################################
		# LOOKUP PATH                                               #
		#############################################################

		file = self.root.lookup(path)

		if not file is None:
			entries.extend(file.readdir())

		#############################################################
		# YIELD ENTRIES                                             #
		#############################################################

		for entry in entries:
			yield fuse.Direntry(entry.encode(FS.FSE))

	#####################################################################

	def unlink(self, path):
		#############################################################
		# LOOKUP PATH                                               #
		#############################################################

		file = self.root.lookup(path)

		if file is None:
			return -errno.ENOENT

		#############################################################
		# REMOVE FILE                                               #
		#############################################################

		return file.unlink()

	#####################################################################

	def readlink(self, path):
		#############################################################
		# LOOKUP PATH                                               #
		#############################################################

		file = self.root.lookup(path)

		if file is None:
			return -errno.ENOENT

		#############################################################
		# GET DATA                                                  #
		#############################################################

		return file.data

	#####################################################################

	def symlink(self, src, dst):
		#############################################################
		# SPLIT DST                                                 #
		#############################################################

		dst_dirname, dst_basename = os.path.split(dst)

		#############################################################
		# LOOKUP PATH                                               #
		#############################################################

		file = self.root.lookup(dst_dirname)

		if file is None:
			return -errno.ENOENT

		#############################################################
		# CREATE SYMBOLIC LINK                                      #
		#############################################################

		file.new_lnk(self, dst_basename).data = src

		#############################################################

		return 0

	#####################################################################

	def open(self, path, flags):
		#############################################################
		# LOOKUP PATH                                               #
		#############################################################

		file = self.root.lookup(path)

		if file is None:
			return -errno.ENOENT

		#############################################################

		return 0

	#####################################################################

	def read(self, path, size, offset):
		#############################################################
		# LOOKUP PATH                                               #
		#############################################################

		file = self.root.lookup(path)

		if file is None:
			return -errno.ENOENT

		if callable(file.data) != False:
			return -errno.ENOSYS

		#############################################################
		# READ DATA                                                 #
		#############################################################

		if offset >= file.stat.st_size:
			return ''

		if size > file.stat.st_size - offset:
			size = file.stat.st_size - offset

		return file.data[offset: offset + size]

	#####################################################################

	def write(self, path, buff, offset):
		#############################################################
		# LOOKUP PATH                                               #
		#############################################################

		file = self.root.lookup(path)

		if file is None:
			return -errno.ENOENT

		if callable(file.data) == False:
			return -errno.ENOSYS

		#############################################################
		# EXECUTE FUNCTION                                          #
		#############################################################

		ret = file.data(path, buff)

		return len(buff) \
			if ret >= 0 else ret

	#####################################################################

	def truncate(self, path, length):
		return 0

#############################################################################
