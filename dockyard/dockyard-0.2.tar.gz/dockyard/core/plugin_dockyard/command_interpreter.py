import os, sys, time
import vagrant
from dockyard.core.command_interpreter import *

class DockyardCommandInterpreter(CommandInterpreter):
    """ Command interpreter for Docker related tasks """

    def init(self, args):
        self.dockyard.init()

    def list(self, args):
        self.dockyard.list()

    def start(self, args):
        for dockyardName in args.dockyard:
            self.dockyard.start(dockyardName)
            self.dns.configure(dockyardName)

    def stop(self, args):
        for dockyardName in args.dockyard:
            self.dockyard.stop(dockyardName)
            self.dns.configure(dockyardName)



