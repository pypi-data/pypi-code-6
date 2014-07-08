import os, sys, time
import vagrant
from dockyard.core.command_interpreter import *

class StackCommandInterpreter(CommandInterpreter):
    """ Command interpreter for Stack related tasks """

    def up(self, args):
        
        # Bring Vagrant UP
        v = vagrant.Vagrant()
        if not v.status()['default'] == 'running':
            self.vagrant.up()

        # Verify Vagrant is UP
        i = 0
        while not v.status()['default'] == 'running':
            print "waiting for Vagrant box.."
            time.sleep(1)
            i = i + 1
            if i > 5:
                print "Something went wrong, Vagrant box is still not up."
                sys.exit(1)

        # Get a list of the docker containers we have built already
        dockerDirs = filter(lambda x: os.path.isdir('docker/' + x), os.listdir('docker'))
        imagesBuilt = [] 
        for imageInfo in self.docker.dockerClient.images():
            imagesBuilt.append(imageInfo['Repository'])

        # Build docker containers
        for dockerName in list(set(dockerDirs) - set(imagesBuilt)):
            self.docker.build(dockerName)

    def down(self, args):
        self.vagrant.destroy()

    def start(self, args):
        for dockName in args.configuration:
            self.dockyard.start(dockName)

        # dockConfig = json.load(open('dock.json'))

        # for dockName in args.configuration:
        #     if not dockConfig['docks'].get(dockName):
        #         print 'No such dock configuration [%s] found.' % dockName
        #         sys.exit(1)
    
        #     run('vagrant ssh --command "python /vagrant/scripts/dns.py %s"' % dockName)

        #     # f = open('','w')
        #     # f.write('')
        #     # f.close()

        #     #dock


    def stop(self, args):

        for id in args.configuration:
            self.dockyard.stop(id)

