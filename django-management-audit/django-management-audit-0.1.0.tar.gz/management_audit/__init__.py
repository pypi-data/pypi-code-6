import sys
import imp
import os

from django.utils.timezone import now
from django.core.management import find_commands

from management_audit.models import Audit


__version__ = '0.1.0'


def install(apps_to_audit, exclude=None):
    importer = CommandImporter(apps_to_audit, exclude)
    sys.meta_path.insert(0, importer)


class CommandImporter(object):

    def __init__(self, apps_to_audit, exclude):
        self.paths = dict()
        self.commands_to_audit = dict()
        for app_name in apps_to_audit:
            commands = self.get_commands(app_name, exclude)
            self.commands_to_audit.update(commands)

    def get_commands(self, app_name, exclude):
        path = os.path.join(app_name, 'management')
        commands = find_commands(path)
        return {self.to_module_name(app_name, c): c for c in commands
            if not exclude or c not in exclude}

    def to_module_name(self, app_name, command):
        return '%s.management.commands.%s' % (app_name, command)

    def find_module(self, fullname, path=None):
        if fullname in self.commands_to_audit:
            self.paths[fullname] = path
            return self
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        command = self.commands_to_audit[fullname]
        module = imp.find_module(command, self.paths[fullname])
        wrapper = CommandModuleWrapper(command, module)
        sys.modules[fullname] = wrapper
        return wrapper


class CommandModuleWrapper(object):

    def __init__(self, command, location):
        module = imp.load_module(command, *location)
        self.command_name = command
        self.command = module.Command

    def __getattr__(self, name):
        if name == 'Command':
            return self._command
        return None

    def _command(self):
        return CommandWrapper(self.command_name, self.command())


class CommandWrapper(object):

    def __init__(self, command_name, command):
        self.command_name = command_name
        self.command = command
        self.old_execute = command.execute
        command.execute = self._execute

    def __getattr__(self, name):
        return getattr(self.command, name)

    def _execute(self, *args, **options):
        date_started = now()
        self.old_execute(*args, **options)
        date_ended = now()
        Audit.objects.create(
            command_name=self.command_name,
            date_started=date_started,
            date_ended=date_ended
        )
