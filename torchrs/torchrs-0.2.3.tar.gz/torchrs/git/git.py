#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Binh Vu <binh@toan2.com>"

import os, subprocess

from ..shell.shell import Shell

class Git(object):

	@staticmethod
	def clone(repo, location, func):
		if os.path.exists(location):
			subprocess.call(["rm", "-rf", location])

		if repo.find("tester/") != -1:
			return Shell.call(["cp", "-a", repo[7:-4], location])

		if func != None:
			return Shell.call(["git", "clone", repo, location], callback=func)
		else:
			return Shell.call(["git", "clone", repo, location])

	@staticmethod
	def isGitRepo(location):
		content = Shell.call(["git", "rev-parse", "--git-dir"])
		for line in content:
			if line.find("fatal") > 0:
				return False
			return True

		assert False, "Error not reach this line"

	@staticmethod
	def parseQuery(url):
		branch = None
		tag = None
		commit = None

		if url.find(".git#") != -1:
			query = url[url.find(".git#") + 5:]
			if query[-1] != "&": query += "&"

			tmp = query.find("branch=") + 7
			if tmp != 6:
				branch = query[tmp:query.find("&", tmp)]
			tmp = query.find("tag=") + 4
			if tmp != 3:
				tag = query[tmp:query.find("&", tmp)]
			tmp = query.find("commit=") + 7
			if tmp != 6:
				commit = query[tmp:query.find("&", tmp)]

		return {
			"host": url[:url.find(".git") + 4],
			"branch": branch,
			"tag": tag,
			"commit": commit
		}

	def isCurrentTag(self, tag):
		pass

	def isCurrentBranch(self, branch):
		pass

	def isCurrentCommit(self, commit):
		pass

	def checkoutBranch(self, branch):
		pass

	def checkoutCommit(self, commit):
		pass

	def checkoutTag(self, tag):
		pass
