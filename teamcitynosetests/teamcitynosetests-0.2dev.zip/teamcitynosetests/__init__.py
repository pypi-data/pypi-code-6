import traceback
import operator
import os
import sys
import logging
from nose.plugins import Plugin
from types import ModuleType


log = logging.getLogger('nose.plugins.teamcityoutput')

def make_service_message(message_name, **kwargs):
    """Create service message"""
    out = ''
    if kwargs is not None:
        for key, value in iter(sorted(kwargs.items())):
            out += "{0}='{1}' ".format(key, escape_message(str(value)))
        out = out.strip()
    if len(kwargs) > 0:
        out = ' ' + out
    return "##teamcity[{0}{1}]".format(message_name, out)

def escape_message(toescape):
    """Escape message according to team city service message specification"""
    out = ''
    for char in list(toescape):
        codepoint = ord(char)
        if codepoint > 127:
            out += "|0x{0:04x}".format(codepoint)
        elif codepoint == 0x0d:
            out += '|r'
        elif codepoint == 0x0a:
            out += '|n'
        elif char == '|':
            out += "||"
        elif char == '[':
            out += '|['
        elif char == ']':
            out += '|]'
        elif char == "'":
            out += "|'"
        else:
            out += char
    return out


def name_of_context(context):
    if isinstance(context, ModuleType):
        return context.__name__
    return context.__module__ + '.' + context.__class__.__name__

class TeamCityOutput(Plugin):
    """Output test results as team city service messages"""
    name = 'teamcitynosetests'

    def configure(self, options, conf):
        Plugin.configure(self, options, conf)
        if not self.enabled:
            return

    def finalize(self, result):
        pass

    def _report(self, message):
        self.stream.writeln(message)

    def setOutputStream(self, stream):
        self.stream = stream
        class dummy():
            def write(self, *arg):
                pass
            def writeln(self, *arg):
                pass
        d = dummy()
        return d

    def formatErr(self, err):
        exctype, value, tb = err
        return ''.join(traceback.format_exception(exctype, value, tb))

    def addFailure(self, test, err):
        self._report(make_service_message(
            'testFailed',
            name=test.shortDescription() or str(test),
            message=self.formatErr(err)))

    def startContext(self, context):
        self._report(make_service_message(
            'testSuiteStarted', 
            name=name_of_context(context)))

    def stopContext(self, context):
        self._report(make_service_message(
            'testSuiteFinished',
            name=name_of_context(context)))
    
    def startTest(self, test):
        self._report(make_service_message(
            'testStarted',
            name=test.shortDescription() or str(test)))

    def stopTest(self, test):
        self._report(make_service_message(
            'testFinished',
            name=test.shortDescription() or str(test)))
