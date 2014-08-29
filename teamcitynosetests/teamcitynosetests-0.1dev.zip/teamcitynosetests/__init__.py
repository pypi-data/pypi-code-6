import traceback
import operator
import os
from nose.plugins import Plugin

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
    return context.__module__ + '.' + context.__class__.__name__

class TeamCityOutput(Plugin):
    """Output test results as team city service messages"""

    name = 'teamcity-output'
    score = 2

    def options(self, parser, env=os.environ):
        super(TeamCityOutput, self).options(parser, env=env)

    def configure(self, options, conf):
        super(TeamCityOutput, self).configure(options, conf)
        if not self.enabled:
            return
    
    def finalize(self, result):
        pass

    def _report(message):
        pass

    def startContext(self, context):
        _report(make_service_message(
            'testSuiteStarted', 
            name=name_of_context(context)))

    def stopContext(self, context):
        _report(make_service_message(
            'testSuiteFinished',
            name=name_of_context(context)))
    
    def startTest(self, test):
        pass

    def stopTest(self, test):
        pass
