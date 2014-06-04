# coding=UTF-8
#
#	Copyright 2014, Marten de Vries
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

from pouchdb.tests.utils import alt_setup
import doctest
import pouchdb
import json

def printjson(data):
	print json.dumps(data, sort_keys=True, default=repr)

def load_tests(loader, tests, ignore):
	paths = ["../objectstorage.py", "../__init__.py", "../mapping.py"]
	for path in paths:
		suite = doctest.DocFileSuite(path, globs={
			"setup": alt_setup,
			"pouchdb": pouchdb,
			"printjson": printjson,
		}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
		tests.addTests(suite)
	return tests
