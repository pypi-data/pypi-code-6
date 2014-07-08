#!/usr/bin/python
import argparse, sys, json, os
import docker
import dockyard.core.lib
from command_interpreter import *

VERSION = '0.1'
DOCKER_URL = 'http://127.0.0.1:5555'
DOCKER_API_VERSION = '1.7'

class NoArgHelpParser(argparse.ArgumentParser):
    """ Extend parser to show help screen whene executed with no arguments """

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)            

# Setup temp directory
try:
    os.mkdir('temp')
except OSError:
    pass

class Cli(object):

    parser = None
    plugins = None
    moduleSubparsers = None

    def __init__(self):

        self.plugins = []

        ### Parse command-line arguments
        self.parser = NoArgHelpParser(description='''Dockyard CLI''',)
        self.moduleSubparsers = self.parser.add_subparsers(dest='module', help='_')

    def addPlugin(self, plugin):
        self.plugins.append(plugin)


    def parse(self):

        for plugin in self.plugins:
            plugin.configureSuppliedParser(self.moduleSubparsers)

        ## Help
        self.parser.add_argument('--version', action='version', version=VERSION, help="Return version of script")
        args = self.parser.parse_args()

        ## Setup command interpreter through reflection
        module = args.module.capitalize() + 'CommandInterpreter'
        commandInterpreter = None
        for cls in CommandInterpreter.__subclasses__():
            if cls.__name__ == module:
                commandInterpreter = cls

        if not commandInterpreter:
            print "Unable to find a command interpreter for [%s]" % module
            sys.exit(1)

        # Inject Dependencies
        dockyardConfig = json.load(open('dockyard.json'))
        dockerClient = docker.Client(base_url=DOCKER_URL, version=DOCKER_API_VERSION)
        dockerWrapper = lib.DockerWrapper(dockerClient=dockerClient)
        vagrantWrapper = lib.VagrantWrapper()
        dockyard = lib.Dockyard(dockyardConfig=dockyardConfig, docker=dockerWrapper, dockerImageFactory=lib.FactoryDockerImage(config=dockyardConfig))
        dns = lib.Dns(dockerClient=dockerClient) 

        commandInterpreter = commandInterpreter( \
            vagrant=vagrantWrapper, \
            docker=dockerWrapper, \
            dockyard=dockyard, \
            dns=dns
        )
        commandInterpreter.execute(args)

