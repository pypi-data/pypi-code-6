import os
import string
from subprocess import call


class BuildCommand(object):
    def __init__(self, command, path, params=None):
        self.command = command
        self.path = path
        self.params = params

    def __call__(self):
        command = string.split(self.command, ' ')
        if self.params:
            for key, value in self.params.iteritems():
                # this option template should be in the yaml file so that the build
                # tools can be swapped in and out properly
                option = "--%s='%s'" % (key, value)
                command.append(option)
            print command
        os.chdir(self.path)
        call(command)

    def execute(self):
        self()
