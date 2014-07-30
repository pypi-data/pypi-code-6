from subprocess import call


class BuildCommand(object):
    def __init__(self, command, params=None):
        self.command = command
        self.params = params

    def __call__(self):
        command = []
        command.append(self.command)
        if self.params:
            for key, value in self.params:
                # this option template should be in the yaml file so that the build
                # tools can be swapped in and out properly
                option = " --%s=%s" % (key, value)
                command.append(option)
            print command
        call(command)

    def execute(self):
        self()
