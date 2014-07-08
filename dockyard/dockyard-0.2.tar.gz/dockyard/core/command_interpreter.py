import os, sys, time
import vagrant

class CommandInterpreter(object):

    vagrant = None
    docker = None
    dockYard = None
    dns = None

    def __init__(self, vagrant=None, docker=None, dockyard=None, dns=None):
        self.vagrant = vagrant
        self.docker = docker
        self.dockyard = dockyard
        self.dns = dns

    def execute(self, args):
        """ Execute command via reflection """
        method = getattr(self, args.operation)
        method(args)        

