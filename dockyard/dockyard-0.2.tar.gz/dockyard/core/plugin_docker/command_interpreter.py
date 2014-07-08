import os, sys, time
import vagrant
from dockyard.core.command_interpreter import *

class DockerCommandInterpreter(CommandInterpreter):
    """ Command interpreter for Docker related tasks """

    def build(self, args):

        # Compile a list of valid dockers to build
        dockers = []
        if 'all' in args.docker:
            dockers = os.listdir('docker')
        else:
            dockers = list(set(args.docker) & set(os.listdir('docker')))
            dockers = filter(lambda x: os.path.isdir('docker/' + x), dockers)

        # Get a list of docker containers that we want to initialize after vagrant comes up        
        for docker in dockers:
            self.docker.build(docker)

    def kill(self, args):        
        for container in args.container:
            self.docker.kill(container)

    def command(self, args):
        print args
        run('vagrant ssh --command "docker %s"' % (' '.join(args.arg)))

    def image(self, args):
        if args.action == 'list':
            self.docker.images()

        elif args.action == 'remove':
            for image in args.image:
                self.docker.removeImageById(image)

        elif args.action == 'run':
            for name in args.image:
                self.docker.runByName(name)

    def container(self, args):
        if args.action == 'list':
            #self.docker.containers()
            self.docker.listContainers()

        elif args.action == 'kill':
            for hash in args.hash:
                self.docker.killContainerById(hash)


