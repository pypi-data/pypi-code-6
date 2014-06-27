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

import os, fuse, stat, pyAMI.exception

#############################################################################

fuse.fuse_python_api = (0, 2)

#############################################################################

TYPE_DIR = 0
TYPE_REG = 1
TYPE_LNK = 2

#############################################################################

class Entry(object):
	#####################################################################

	_ino_cnt = 0

	#####################################################################

	@classmethod
	def new_dir_stat(cls, mode):
		#############################################################
		# ALLOC_INIT STAT                                           #
		#############################################################

		result = fuse.Stat()

		result.st_ino = cls._ino_cnt
		result.st_mode = stat.S_IFDIR | mode
		result.st_size = 0
		result.st_nlink = 2

		result.st_uid = os.geteuid() if hasattr(os, 'geteuid') else 0
		result.st_gid = os.getegid() if hasattr(os, 'getegid') else 0

		#############################################################
		# INCREMENT INODE COUNTER                                   #
		#############################################################

		cls._ino_cnt += 1

		#############################################################

		return result

	#####################################################################

	@classmethod
	def new_reg_stat(cls, mode):
		#############################################################
		# ALLOC_INIT STAT                                           #
		#############################################################

		result = fuse.Stat()

		result.st_ino = cls._ino_cnt
		result.st_mode = stat.S_IFREG | mode
		result.st_size = 0
		result.st_nlink = 1

		result.st_uid = os.geteuid() if hasattr(os, 'geteuid') else 0
		result.st_gid = os.getegid() if hasattr(os, 'getegid') else 0

		#############################################################
		# INCREMENT INODE COUNTER                                   #
		#############################################################

		cls._ino_cnt += 1

		#############################################################

		return result

	#####################################################################

	@classmethod
	def new_lnk_stat(cls, mode):
		#############################################################
		# ALLOC_INIT STAT                                           #
		#############################################################

		result = fuse.Stat()

		result.st_ino = cls._ino_cnt
		result.st_mode = stat.S_IFLNK | mode
		result.st_size = 0
		result.st_nlink = 1

		result.st_uid = os.geteuid() if hasattr(os, 'geteuid') else 0
		result.st_gid = os.getegid() if hasattr(os, 'getegid') else 0

		#############################################################
		# INCREMENT INODE COUNTER                                   #
		#############################################################

		cls._ino_cnt += 1

		#############################################################

		return result

	#####################################################################

	def __init__(self, fs, parent, epyt, name, mode = None):
		super(Entry, self).__init__()

		#############################################################
		# INIT ENTRY                                                #
		#############################################################

		self._parent = parent
		self._name = name
		self._data = None
		self._dirs = {}

		#############################################################

		if   epyt == TYPE_DIR:

			if mode is None:
				mode = 0o755

			self._stat = Entry.new_dir_stat(mode = mode)

		elif epyt == TYPE_REG:

			if mode is None:
				mode = 0o444

			self._stat = Entry.new_reg_stat(mode = mode)

		elif epyt == TYPE_LNK:

			if mode is None:
				mode = 0o444

			self._stat = Entry.new_lnk_stat(mode = mode)

		else:
			raise pyAMI.exception.Error('invalid file type')

	#####################################################################

	def new_dir(self, fs, name, mode = None):
		result = Entry(fs, self, TYPE_DIR, name, mode = mode)

		self._dirs[name] = result

		return result

	#####################################################################

	def new_reg(self, fs, name, mode = None):
		result = Entry(fs, self, TYPE_REG, name, mode = mode)

		self._dirs[name] = result

		return result

	#####################################################################

	def new_lnk(self, fs, name, mode = None):
		result = Entry(fs, self, TYPE_LNK, name, mode = mode)

		self._dirs[name] = result

		return result

	#####################################################################

	def lookup(self, path):
		result = self

		for part in path.split('/'):

			if part:
				#############################################
				# LOOKUP PATH                               #
				#############################################

				result = result._dirs.get(part, None)

				if result is None:
					return None

				#############################################
				# RESOLVE LINK                              #
				#############################################

				if result.type == TYPE_LNK:

					result = self.lookup(result._data)

					if result is None:
						return None

				#############################################

		return result

	#####################################################################

	def readdir(self):
		return list(self._dirs.keys())

	#####################################################################

	def unlink(self):

		if not self._parent is None:
			del self._parent._dirs[self._name]

	#####################################################################

	@property
	def stat(self):
		return self._stat

	#####################################################################

	@property
	def data(self):
		return self._data

	#####################################################################

	@data.setter
	def data(self, data):

		if callable(data):
			###### DO NOT ENCODE ######

			self.        _data = data
			self._stat.st_size = int(0x00)

		else:
			data = data.encode('utf-8')

			self.        _data = data
			self._stat.st_size = len(data)

	#####################################################################

	@property
	def type(self):

		if self._stat.st_mode & stat.S_IFDIR == stat.S_IFDIR:
			return TYPE_DIR

		if self._stat.st_mode & stat.S_IFREG == stat.S_IFREG:
			return TYPE_REG

		if self._stat.st_mode & stat.S_IFLNK == stat.S_IFLNK:
			return TYPE_LNK

#############################################################################
