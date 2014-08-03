### FIXME put getconf, setconf, getinfo all into just a "cmd" command, like:
### carml cmd getinfo foo bar baz
### carml cmd setinfo UseBridges 1
### carml cmd signal newnym

import os
import functools

import zope.interface
from twisted.python import usage
from twisted.internet import defer, reactor

import txtorcon

from interface import ISubCommand
import subcommands

class SetconfOptions(usage.Options):
    def __init__(self):
        super(SetconfOptions, self).__init__()
        self.longOpt.remove('version')
        self.longOpt.remove('help')
        self.args = None

    def parseArgs(self, *args):
        self.args = args

    def getUsage(self, **kw):
        return "Options:\n   Pass options in pairs: name value. Mind your quoting. If there's just one option and it is a single - character then stdin is read and each line interpreted like \"ConfigOption arg0 arg1 argn\"."

## see cmd_info for an alternate way to implement this via a method
## with attributes and "zope.interface.implementsDirectly()"
## trying out both ways to see what feels better
class SetconfSubCommand(object):
    zope.interface.implements(ISubCommand)

    ## Attributes specified by ISubCommand
    options_class = SetconfOptions
    help_text = 'Run one or more SETCONF commands.'
    build_state = False
    load_routers = False

    def validate(self, options, mainoptions):
        if len(options.args) % 2:
            if options.args[0] != '-':
                raise RuntimeError("Specify options in pairs, or - to read stdin.")

    @defer.inlineCallbacks
    def __call__(self, options, proto):
        """
        ISubCommand API
        """

        if False:
            valid_names = yield proto.get_info("config/names")
            valid_names = valid_names['config/names'].strip().split('\n')
            all_names = [line.split() for line in valid_names]
            valid_names = {}
            for (name, cfgtype) in all_names:
                valid_names[name] = cfgtype

        res = yield proto.set_conf(*options.args)
        log.msg(res)
        reactor.stop()

subcommands.register('setconf', SetconfSubCommand())
