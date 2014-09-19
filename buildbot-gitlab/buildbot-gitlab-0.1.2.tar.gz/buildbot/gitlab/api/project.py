#!/usr/bin/env python
# encoding: utf-8


# Copyright (c) 2014, VCA Technology. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import json
import collections
import io

# Converts python2/3 strings to unicode
def convert(data):
    try:
        bs = basestring
    except NameError:
        bs = str
    if isinstance(data, bs):
        return unicode(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

#project json interface
class Json:

    def __init__(self, filename, baseRepoUrl):
        self.data = {}
        self.filename = filename
        self._readFile()
        self.baseRepoUrl = baseRepoUrl

    def __getitem__(self, key):
        if isinstance(key, int):
            key = self.data.keys()[key]
            return { key: self.data[key] }

        if key not in self.data:
            self.data[key] = []

        return Data(key, self.data[key], self)

    def __setitem__(self, key, value):
        if key is None or not key:
            raise ValueError('Invalid namespace: %r' % (key))

        if value is None or not value:
            raise ValueError(format('Invalid project name: %r for namespace: %r' % (value, key)))

        if not isinstance(value, list):
            value = [value]

        self.data[key] = value

        self._saveFile()

    def __iadd__(self, other):
        if other is None or not other:
            raise ValueError('Attempted to add project with no name')

        if other in self.data:
            return self.data.keys()

        self.data[other] = []

        return self.data.keys()

    def __contains__(self, item):
        return item in self.data

    def __delitem__(self, key):
        del self.data[key]

        self._saveFile()

    def __repr__(self):
        return repr(self.filename) + repr(self.data)

    def _saveFile(self):
        self._verifyFile()
        self._writeFile()

    def _verifyFile(self):

        """
        Sanity checks the data to ensure that there arnt any empty namespaces
        :return: None
        """

        for namespace,projects in self.data.iteritems():
            if len(projects) == 0:
                raise Exception('Namespace %r has no projects' % namespace)

    def _writeFile(self):
        with io.open(self.filename, mode='w', encoding='utf-8') as jsonFile:
            jsonFile.write(unicode(json.dumps(self.data)))

    def _readFile(self):
        input = file(self.filename, 'r')
        self.data = convert(json.loads(input.read().decode('utf-8')))

class Data:

    def __init__(self, namespace, projects, json):

        """
        Creates a dictionary of projectNames to repo urls
        :param namespace:
        :param projects:
        :param json:
        :return:
        """

        self.projects = {}
        self.namespace = namespace
        self.json = json

        for project in projects:
            if not isinstance(project, str) and not isinstance(project, unicode):
                raise Exception(format('invalid value: %r' % (type(project))))

            self.projects[project] = self.__createRepoUrl(project)



    def __iadd__(self, other):

        """
        allows addition of 1 or more projects, checks for duplicates
        & raises exception if found.
        :param other: string or list of strings
        :return: list of projects, used to update Json
        """

        if other is None or not other:
            raise ValueError('Attempted to add project with no name')

        if isinstance(other, list):
            for project in other:
                if project in self.projects.keys():
                    raise ValueError('The project %r was already added: %r' % (other, self.projects.keys()))

                self.projects[project] = self.__createRepoUrl(project)
        else:
            if other in self.projects.keys():
                raise ValueError('The project %r was already added: %r' % (other, self.projects.keys()))

            self.projects[other] = self.__createRepoUrl(other)

        return self.projects.keys()

    def __contains__(self, item):
        return item in self.projects.keys()

    def __delitem__(self, item):
        del self.projects[item]

        # unlike __iadd__ the return value doesnt filter back into the Json object as an
        # assignment, so we have to explicitly force an update.
        self.json[self.namespace] = self.projects.keys()

        return self.projects.keys()

    def __getitem__(self, item):
        return  self.projects[item]

    def __createRepoUrl(self, project):
        return ('git@%s:%s/%s.git' % (self.json.baseRepoUrl, self.namespace.replace(' ', '.'), project)).encode("ascii")

