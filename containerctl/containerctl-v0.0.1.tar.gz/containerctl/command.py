"""Container commands."""
import sys
import yaml
from . import Container
from .errors import Error
from clank import ArgumentCommand, HelpCommand, Manager, UsageCommand


def get_containers():
    return sorted(Container.list(), key=lambda c: c.name)


def get_container(name):
    cnts = filter(lambda c: c.name == name, get_containers())
    if cnts:
        return cnts[0]
    return None


class InfoCommand(ArgumentCommand):
    """Print information about a container."""
    name = 'info'

    def add_arguments(self):
        self.argparser.add_argument('-r', '--raw', dest='raw', action='store_true',
                                    help="Use the raw container congfiguration.")
        self.argparser.add_argument('-k', '--key', dest='key', nargs=1,
                                    help="Output only the specified toplevel key.")
        self.argparser.add_argument('path', metavar='PATH', nargs='?',
                                    help="Use this path instead of the current directory.")

    def run(self, args):
        self.parse_args(args)
        try:
            container = Container.from_path(path=self.options.path)
            data = container.to_dict(self.options.raw)
            if self.options.key:
                data = data.get(self.options.key)
            if isinstance(data, (list, tuple, dict)):
                sys.stdout.write(yaml.safe_dump(
                    data, explicit_start=False, default_flow_style=False))
            else:
                print(data)
        except Error as e:
            print("error: {}".format(e))
            return 1


class BuildCommand(ArgumentCommand):
    """Build a container."""
    name = 'build'

    def add_arguments(self):
        self.argparser.add_argument('-p', '--push', dest='push', action='store_true',
                                    help="Push the image after building.")
        self.argparser.add_argument('-P', '--no-prebuild', dest='prebuild', action='store_false',
                                    help="Do not run the container's prebuild.")
        self.argparser.add_argument('-C', '--no-cache', dest='nocache', action='store_true',
                                    help="Do not use the Docker cache.")
        self.argparser.add_argument('-v', '--version', dest='version', nargs=1,
                                    help="The version of the container to build.")
        self.argparser.add_argument('path', metavar='PATH', nargs='?',
                                    help="The path to the container to build.")

    def run(self, args):
        self.parse_args(args)
        try:
            container = Container.from_path(path=self.options.path, version=self.options.version)
            container.build(self.options.prebuild, self.options.nocache)
            print("{} built".format(container.tag))
            if self.options.push:
                container.push()
                print("{} pushed".format(container.tag))
            return 0
        except Error as e:
            print("error: {}".format(e))
            return 1


class PushCommand(ArgumentCommand):
    """Push a container. The container will be built if it necessary."""
    name = 'push'

    def add_arguments(self):
        self.argparser.add_argument('-v', '--version', dest='version', nargs=1,
                                    help="The version of the container to build.")
        self.argparser.add_argument('path', metavar='PATH', nargs='?',
                                    help="The path to the container to push.")

    def run(self, args):
        self.parse_args(args)
        try:
            container = Container.from_path(path=self.options.path, version=self.options.version)
            if not container.built:
                container.build()
            container.push()
            print("{} pushed".format(container.tag))
            return 0
        except Error as e:
            print("error: {}".format(e))
            return 1


class RemoveCommand(ArgumentCommand):
    """Remove a container."""
    name = 'rm'

    def add_arguments(self):
        self.argparser.add_argument('-v', '--version', dest='version', nargs=1,
                                    help="The version of the container to remove.")
        self.argparser.add_argument('path', metavar='PATH', nargs='?',
                                    help="The path to the container to remove.")

    def run(self, args):
        self.parse_args(args)
        try:
            container = Container.from_path(path=self.options.path)
            if container.built:
                container.rm()
                print ("{} removed".format(container.tag))
                return 0
            else:
                print ("{} not found".format(container.tag))
                return 2
        except Error as e:
            print("error: {}".format(e))
            return 1


class RunCommand(ArgumentCommand):
    """Run a container."""
    name = 'run'

    def add_arguments(self):
        self.argparser.add_argument('-d', '--detach', dest='detach', action='store_true',
                                    help="Run the container in the background.")
        self.argparser.add_argument('-v', '--version', dest='version', nargs=1,
                                    help="The version of the container to run.")
        self.argparser.add_argument('path', metavar='PATH', nargs='?',
                                    help="The path to the container to run.")

    def run(self, args):
        self.parse_args(args)
        try:
            container = Container.from_path(path=self.options.path, version=self.options.version)
            if not container.built:
                container.build()
                print("{} built".format(container.tag))
            container.run(self.options.detach)
            if self.options.detach:
                print("{} running".format(container.tag))
        except Error as e:
            print("error: {}".format(e))
            return 1


class KillCommand(ArgumentCommand):
    """Kill a container."""
    name = 'kill'

    def add_arguments(self):
        self.argparser.add_argument('path', metavar='PATH', nargs='?',
                                    help="The path to the container to kill.")

    def run(self, args):
        self.parse_args(args)
        try:
            container = Container.from_path(path=self.options.path)
            container.kill()
            print("{} killed".format(container.tag))
        except Error as e:
            print("error: {}".format(e))
            return 1



def run():
    """Run the ops tool."""
    return Manager([
        BuildCommand,
        HelpCommand,
        InfoCommand,
        KillCommand,
        PushCommand,
        RemoveCommand,
        RunCommand,
        UsageCommand,
    ]).run()
