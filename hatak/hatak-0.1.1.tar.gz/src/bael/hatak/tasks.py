from os import mkdir, path
from glob import glob

from bael.project.virtualenv import VirtualenvTask
from baelfire.application.commands.init.models import InitFile
from baelfire.dependencies import (
    AlwaysRebuild,
    FileDoesNotExists,
    FileChanged,
)
from baelfire.error import CommandError
from baelfire.task import Task


class CreateDataDir(Task):
    name = 'Creating data directory'
    path = '/data'

    directorie_names = [
        'data',
    ]

    @property
    def directories(self):
        for name in self.directorie_names:
            yield self.paths[name]

    def generate_dependencies(self):
        for directory in self.directories:
            self.add_dependecy(FileDoesNotExists(directory))

    def make(self):
        for directory in self.directories:
            if not path.exists(directory):
                mkdir(directory)


class Develop(Task):

    def generate_links(self):
        self.add_link('bael.hatak.templates:FrontendIni')
        self.add_link('bael.project.virtualenv:Develop')
        self.add_link(Migration)


class Serve(VirtualenvTask):
    name = 'Run development server'
    path = '/serve'

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def generate_links(self):
        self.add_link(Develop)

    def make(self):
        self.pserve('%(data:frontend.ini)s --reload' % (self.paths))

    def pserve(self, command, *args, **kwargs):
        command = self.paths['exe:pserve'] + ' ' + command
        return self.command([command], *args, **kwargs)


class Shell(VirtualenvTask):
    name = 'Run development shell'
    path = '/shell'

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def generate_links(self):
        self.add_link(Develop)

    def make(self):
        self.pshell('%(data:frontend.ini)s' % (self.paths))

    def pshell(self, command, *args, **kwargs):
        command = self.paths['exe:pshell'] + ' ' + command
        return self.command([command], *args, **kwargs)


class MigrationBase(VirtualenvTask):

    def migration(self, command, *args, **kwargs):
        command = self.paths['migration:manage'] + ' ' + command
        return self.python(command, *args, **kwargs)

    def migrate(self, command, *args, **kwargs):
        command = self.paths['exe:migrate'] + ' ' + command
        return self.command([command], *args, **kwargs)


class MigrationData(MigrationBase):

    def get_output_file(self):
        return self.paths['migration:main']

    def make(self):
        self.migrate('create %(migration:main)s "project!"' % self.paths)


class MigrationVersioning(MigrationBase):
    path = '/migration/versioning'

    def get_output_file(self):
        return self.paths['flags:dbversioning']

    def generate_links(self):
        self.add_link('bael.hatak.templates:FrontendIni')
        self.add_link('bael.project.virtualenv:Develop')
        self.add_link('bael.hatak.templates:MigrationManage')
        self.add_link(ProjectTemplates)

    def make(self):
        try:
            self.migration('version_control')
        except CommandError:
            pass
        self.touchme()


class Migration(MigrationBase):
    path = '/migration'

    def generate_dependencies(self):
        super().generate_dependencies()
        for file_ in glob(path.join(self.paths['migration:versions'], '*.py')):
            self.add_dependecy(FileChanged(file_))

    def get_output_file(self):
        return self.paths['flags:dbmigration']

    def generate_links(self):
        self.add_link(MigrationVersioning)

    def make(self):
        self.migration('upgrade')
        self.touchme()


class MigrationScript(MigrationBase):
    path = '/script'

    def generate_dependencies(self):
        super().generate_dependencies()
        self.add_dependecy(AlwaysRebuild())

    def generate_links(self):
        self.add_link(MigrationVersioning)

    def make(self):
        description = self.ask_for('description', 'Migration description')
        self.migration('script "%s"' % (description,))


class BaelfireInitFile(Task):

    path = '/initfile'

    def get_output_file(self):
        return InitFile.filename

    def make(self):
        initfile = InitFile()
        initfile.assign('bael.hatak.recipe:HatakRecipe')
        initfile.save()


class ProjectTemplates(Task):

    path = '/templates'

    def generate_links(self):
        self.add_link('bael.hatak.templates:InitPy')
        self.add_link('bael.hatak.templates:Routes')
        self.add_link('bael.hatak.templates:Settings')
