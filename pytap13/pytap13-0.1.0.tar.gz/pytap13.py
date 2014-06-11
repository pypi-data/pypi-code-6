# Copyright 2013, Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Author: Josef Skladanka <jskladan@redhat.com>

import re
import yamlish
import StringIO



RE_VERSION = re.compile(r"^\s*TAP version 13\s*$")
RE_PLAN = re.compile(r"^\s*(?P<start>\d+)\.\.(?P<end>\d+)\s*(#\s*(?P<explanation>.*))?\s*$")
RE_TEST_LINE = re.compile(r"^\s*(?P<result>(not\s+)?ok)\s*(?P<id>\d+)?\s*(?P<description>[^#]+)?\s*(#\s*(?P<directive>TODO|SKIP)?\s*(?P<comment>.+)?)?\s*$",  re.IGNORECASE)
RE_EXPLANATION = re.compile(r"^\s*#\s*(?P<explanation>.+)?\s*$")
RE_YAMLISH_START = re.compile(r"^\s*---.*$")
RE_YAMLISH_END = re.compile(r"^.*\.\.\.\s*$")


class Test(object):
    def __init__(self, result, id, description = None, directive = None, comment = None):
        self.result = result
        self.id = id
        self.description = description
        try:
            self.directive = directive.upper()
        except AttributeError:
            self.directive = directive
        self.comment = comment
        self.yaml = None
        self._yaml_buffer = None
        self.diagnostics = []


class TAP13(object):
    def __init__(self):
        self.tests = []
        self.__tests_counter = 0
        self.tests_planned = None


    def _parse(self, source):
        seek_version = True
        seek_plan = False
        seek_test = False

        in_test = False
        in_yaml = False
        for line in source:
            if not seek_version and RE_VERSION.match(line):
                raise ValueError("Bad TAP format, multiple TAP headers")

            if in_yaml:
                if RE_YAMLISH_END.match(line):
                    self.tests[-1]._yaml_buffer.append(line.strip())
                    in_yaml = False
                    self.tests[-1].yaml = yamlish.load(self.tests[-1]._yaml_buffer)
                else:
                    self.tests[-1]._yaml_buffer.append(line.rstrip())
                continue

            line = line.strip()

            if in_test:
                if RE_EXPLANATION.match(line):
                    self.tests[-1].diagnostics.append(line)
                    continue
                if RE_YAMLISH_START.match(line):
                    self.tests[-1]._yaml_buffer = [line.strip()]
                    in_yaml = True
                    continue

            # this is "beginning" of the parsing, skip all lines until
            # version is found
            if seek_version:
                if RE_VERSION.match(line):
                    seek_version = False
                    seek_plan = True
                    seek_test = True
                else:
                    continue

            if seek_plan:
                m = RE_PLAN.match(line)
                if m:
                    d = m.groupdict()
                    self.tests_planned = int(d.get('end', 0))
                    seek_plan = False

                    # Stop processing if tests were found before the plan
                    #    if plan is at the end, it must be the last line -> stop processing
                    if self.__tests_counter > 0:
                        break

            if seek_test:
                m = RE_TEST_LINE.match(line)
                if m:
                    self.__tests_counter += 1
                    t_attrs = m.groupdict()
                    if t_attrs['id'] is None:
                        t_attrs['id'] = self.__tests_counter
                    t_attrs['id'] = int(t_attrs['id'])
                    if t_attrs['id'] < self.__tests_counter:
                        raise ValueError("Descending test id on line: %r" % line)
                    # according to TAP13 specs, missing tests must be handled as 'not ok'
                    # here we add the missing tests in sequence
                    while t_attrs['id'] > self.__tests_counter:
                        self.tests.append(Test('not ok', self.__tests_counter, comment = 'DIAG: Test %s not present' % self.__tests_counter))
                        self.__tests_counter += 1
                    t = Test(**t_attrs)
                    self.tests.append(t)
                    in_test = True
                    continue

        if self.tests_planned is None:
            # TODO: raise better error than ValueError
            raise ValueError("Missing plan in the TAP source")

        if len(self.tests) != self.tests_planned:
            for i in range(len(self.tests), self.tests_planned):
                self.tests.append(Test('not ok', i+1, comment = 'DIAG: Test %s not present'))


    def parse(self, source):
        if isinstance(source, (str, unicode)):
            self._parse(StringIO.StringIO(source))
        elif hasattr(source, "__iter__"):
            self._parse(source)

if __name__ == "__main__":
    input = """
    TAP version 13
    ok 1 - Input file opened
    not ok 2 - First line of the input valid
        ---
        message: 'First line invalid'
        severity: fail
        data:
          got: 'Flirble'
          expect: 'Fnible'
        ...
    ok - Read the rest of the file
    not ok 5 - Summarized correctly # TODO Not written yet
        ---
        message: "Can't make summary yet"
        severity: todo
        ...
    ok  Description
    # Diagnostic
        ---
        message: 'Failure message'
        severity: fail
        data:
        got:
            - 1
            - 3
            - 2
        expect:
            - 1
            - 2
            - 3
    ...
    1..6
"""
    t = TAP13()
    t.parse(input)

    import pprint
    for test in t.tests:
        print test.result, test.id, test.description, "#", test.directive, test.comment
        pprint.pprint(test._yaml_buffer)
        pprint.pprint(test.yaml)
