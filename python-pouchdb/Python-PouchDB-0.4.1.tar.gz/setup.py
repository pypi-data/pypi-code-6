#!/usr/bin/env python
#
#	Copyright 2013-2014, Marten de Vries
#
#	Licensed under the Apache License, Version 2.0 (the "License");
#	you may not use this file except in compliance with the License.
#	You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
#	Unless required by applicable law or agreed to in writing, software
#	distributed under the License is distributed on an "AS IS" BASIS,
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	See the License for the specific language governing permissions and
#	limitations under the License.

from setuptools import setup, Command
import os
import shlex
import subprocess

info = {}
with open(os.path.join("pouchdb", "info.py")) as f:
	exec(f.read(), info)

class ScriptCommand(Command):
	user_options = []
	working_dir = "."

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		os.chdir(self.working_dir)
		self.execute(subprocess.call, [shlex.split(self.script)])

class BuildPluginsJSCommand(ScriptCommand):
	working_dir = "js"
	script = "./build-plugins"
	description = "Builds all JavaScript plug-ins that are developed alongside Python-PouchDB."

class BuildBundleJSCommand(ScriptCommand):
	working_dir = "js"
	script = "./build-bundle"
	description = "Builds the JavaScript bundle of all JS code that Python-PouchDB needs."

class WatchBundleJSCommand(ScriptCommand):
	working_dir = "js"
	script = "./watch-bundle"
	description = "Builds and keeps up-to-date the JavaScript bundle of all JS code that Python-PouchDB needs."

class BuildAllJSCommand(ScriptCommand):
	working_dir = "js"
	script = "./build-all"
	description = "Builds plug-in and bundle JavaScript files."

class JSHintCommand(ScriptCommand):
	working_dir = "js"
	script = "./run-jshint"
	description = "Test all JavaScript files using JSHint for style errors."

class NodeTestsCommand(ScriptCommand):
	working_dir = "js/"
	script = "./run-test"
	description = "Runs the NodeJS tests for the plug-ins. (Only a few basic checks.)"

class NodeDependenciesCommand(ScriptCommand):
	working_dir = "js"
	script = "./install-node-dependencies"
	description = "Install all node dependencies for the modules in the js subdirectory."

class ExtensiveTestCommand(ScriptCommand):
	script = "python runtests.py"
	description = "Run the test suite generating Python coverage and with different Python/Qt versions."

class SimpleTestCommand(ScriptCommand):
	script = "python -m unittest pouchdb.tests"
	description = "Run the test suite in one version of Python with only one type of Qt binding."

class JSCoverageCommand(ScriptCommand):
	script = "python jscoverage.py"
	description = "Runs the basic test suite and gathers JS coverage info."

setup(
	name=info["name"],
	version=info["__version__"],
	description="A Python interface to PouchDB",
	long_description="""Python-PouchDB provides an interface to all the
goodness of the PouchDB JavaScript library (http://pouchdb.com/). It's
released under the Apache License v2 and it also offers a synchronous
API.

Uses QtWebKit internally, so either PySide, PyQt4 or PyQt5 is required.""",
	author=info["__author__"],
	author_email="marten@openteacher.org",
	url="http://python-pouchdb.marten-de-vries.nl/",
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
		"Operating System :: POSIX",
		"Programming Language :: JavaScript",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
		"Topic :: Database",
		"Topic :: Software Development :: Libraries",
	],
	packages=["pouchdb", "pouchdb.tests"],
	package_data={
		"pouchdb": ["bundle.js"],
	},
	install_requires=[
		"jsonpickle",
		"python-dateutil",
	],
	test_suite="pouchdb.tests",
	use_2to3=True,
	cmdclass={
		"build_plugins_js": BuildPluginsJSCommand,
		"build_bundle_js": BuildBundleJSCommand,
		"watch_bundle_js": WatchBundleJSCommand,
		"build_all_js": BuildAllJSCommand,
		"jshint": JSHintCommand,
		"node_tests": NodeTestsCommand,
		"install_node_dependencies": NodeDependenciesCommand,
		"extensive_test": ExtensiveTestCommand,
		"test": SimpleTestCommand,
		"js_coverage": JSCoverageCommand,
	},
)
