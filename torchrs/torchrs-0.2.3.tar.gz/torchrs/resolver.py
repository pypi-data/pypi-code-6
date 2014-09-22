#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Binh Vu <binh@toan2.com>"

import json, sys, os

from .util import getlogger
from .git.git import Git 
from .shell.shell import Shell
from .module.module import Module

class Resolver(object):

	def __init__(self, abspath):
		with open(abspath, 'r') as f:
			self.dep = json.loads(f.read())

		self.root   = os.path.dirname(abspath)

		self.extra	= {
			"root": self.root
		}

		self.logger = getlogger("torch.resolver")
		self.git 	= Git()

		self.modules = set()

	def resolve(self):
		if "dependencies" not in self.dep:
			self.dep["dependencies"] = {}
		if not os.path.exists(os.path.join(self.root, "modules")):
			os.mkdir(os.path.join(self.root, "modules"))

		self.logger.info("RESOLVE PACKAGES")

		for package, conf in self.dep["dependencies"].iteritems():
			conf["name"] = package

			self.logger.info("RESOLVE PACKAGE: {0}".format(package))

			if Module.isTorchModule(conf):
				if not self.resolveTorchPackage(conf):
					self.logger.info("CANNOT RESOLVE PACKAGE {0}".format(package))
					exit(0)
			else:
				if not self.resolvePythonPackage(conf):
					self.logger.info("CANNOT RESOLVE PACKAGE {0}".format(package))
					exit(0)

			self.logger.info("RESOLVED!")

		self.logger.info("RESOLVE PACKAGES FINISH!")

		self.logger.info("Write config")
		
		module = Module(self.root)
		module.updateModuleConfig([os.path.join(self.root, "modules")])
		module.postProcess(self.dep, self.extra)
		self.logger.info("FINISH!")


	"""
		Resolve torch module

		@param dict config
		@return boolean resolve success or not
	"""
	def resolveTorchPackage(self, config):
		package = config["name"]
		packageDir = os.path.join(self.root, "modules", package)

		if not os.path.exists(packageDir):
			os.mkdir(packageDir)

		if package in self.modules:
			self.logger.debug("Package {0} has been installed before".format(package))
			return True 

		module = Module(packageDir)

		res = module.verify()
		if not res[0]:
		 	self.logger.debug("Package {0} was invalid due to: {1}".format(package, res[1]))

			self.logger.debug("Install package {0} ...".format(package))
			if self.installFromGit(packageDir, config) == False:
				return False
			
			res = module.verify()
			if not res[0]:
				self.logger.error("After install, package {0} is invalid due to {1}".format(package, res[1]))
				return False

		self.modules.add(package)
		for dependency in module.getDependencies():
			self.logger.debug("Resolve dependency {0}".format(dependency["name"]))

			if self.resolveTorchPackage(dependency) == False:
				self.logger.debug("Cannot resolve dependency {0}".format(dependency["name"]))
				return False
			else:
				self.modules.add(dependency["name"])

		# module.updateModuleConfig([os.path.join(self.root, "modules")])
		module.postProcess(config, self.extra)
		
	 	return True

	"""
		Resolve python package

		@param dict config configuration 
		@return boolean indicate success or not
	"""
	def resolvePythonPackage(self, config):
		package = config["name"]
		content = Shell.call(["pip", "show", package], callback=self.logger.debug)

		if len(content) != 0:
			self.logger.info("Package {0} has been installed before".format(package))
			return True

		return self.installFromPip(config)

	"""
		Install module from Git and update the working tree according to the configuration

		@param string packageDir location of package 
		@param dict conf configuration
		@return boolean indicate success or not
	"""
	def installFromGit(self, packageDir, conf):
		package = conf["name"]
		data = Git.parseQuery(conf["host"])

		content = self.git.clone(data["host"], packageDir, self.logger.debug)
		for line in content:
			if line.find("fatal: ") != -1 or line.find("error: ") != -1:
				return False

		module = Module(packageDir)
		res = module.verify()
		if not res[0]:
			self.logger.debug("After install from Git Repo, package {0} is still invalid due to: {1}".format(package, res[1]))
			return False

		res = module.updateModuleStatus(data)
		if not res[0]:
			self.logger.debug("Cannot update working tree of package {0} due to: {1}".format(package, res[1]))

		return True

	"""
		Install module by pip

		@param dict conf configuration
		@return boolean
	"""
	def installFromPip(self, conf):
		content = Shell.call(["pip", "install", conf["name"]], self.logger.debug)
		for line in content:
			if line.find("Could not find any downloads") != -1:
				return False

			if line.find("Permission denied") != -1:
				return False

		return True