from bael.project.recipe import ProjectRecipe
from baelfire.application.application import Application
from baelfire.recipe import Recipe

from .tasks import (
    CreateDataDir,
    Serve,
    MigrationVersioning,
    Migration,
    BaelfireInitFile,
    MigrationData,
    ProjectTemplates,
    Develop,
    Shell,
    MigrationScript,
)
from .templates import (
    MigrationManage,
    InitPy,
    Routes,
    Settings,
    FrontendIni,
)

from .uwsgi import (
    UwsgiStart,
    UwsgiStop,
    UwsgiRestart,
)


class HatakRecipe(Recipe):

    prefix = '/hatak'

    def create_settings(self):
        self.set_path('project:src', 'cwd', 'src')
        self.set_path('data', 'cwd', 'data')
        self.set_path('data:frontend.ini', 'data', 'frontend.ini')
        self.set_path('data:log', 'data', 'all.log')
        self.set_path('uwsgi:socket', None, '/tmp/uwsgi.socket')
        self.set_path('uwsgi:pid', 'data', 'uwsgi.pid')
        self.set_path(
            'venv:site-packages',
            'virtualenv_path',
            'lib/python3.4/site-packages/')

        self.set_path('flags:dbversioning', 'flags', 'versioning.flag')
        self.set_path('flags:dbmigration', 'flags', 'dbmigration.flag')

        self.set_path('migration:main', 'cwd', 'migrations')
        self.set_path('migration:manage', 'migration:main', 'manage2.py')
        self.set_path('migration:versions', 'migration:main', 'versions')

        self.set_path('exe:migrate', 'virtualenv:bin', 'migrate')
        self.set_path('exe:pserve', 'virtualenv:bin', 'pserve')
        self.set_path('exe:pshell', 'virtualenv:bin', 'pshell')
        self.set_path('exe:uwsgi', 'virtualenv:bin', 'uwsgi')

        self.settings['develop'] = True

        self.set_path('project:application', 'project:home', 'application')
        self.set_path('project:initpy', 'project:application', 'init.py')
        self.set_path('project:settings', 'project:application', 'settings')
        self.set_path('project:routes', 'project:application', 'routes.py')
        self.set_path('project:default', 'project:settings', 'default.py')

    def final_settings(self):
        self.set_path('virtualenv_path', 'cwd', 'venv')
        self.set_path('flags', 'data', 'flags')

        self.settings['packages'] = [
            'sqlalchemy-migrate',
            'hatak',
            'waitress',
            'pyramid_debugtoolbar',
            'pyramid_beaker',
            'pyramid_jinja2',
            'uwsgi']
        self.settings['directories'].append('project:application')
        self.settings['directories'].append('project:settings')
        self.settings['entry_points'] = (
            '[paste.app_factory]\n'
            '\t\tmain = %(package:name)s.application.init:main')

    def gather_recipes(self):
        self.add_recipe(ProjectRecipe(False))

    def gather_tasks(self):
        self.add_task(CreateDataDir)
        self.add_task(FrontendIni)
        self.add_task(Serve)
        self.add_task(MigrationVersioning)
        self.add_task(Migration)
        self.add_task(BaelfireInitFile)
        self.add_task(MigrationData)
        self.add_task(MigrationManage)
        self.add_task(InitPy)
        self.add_task(Routes)
        self.add_task(ProjectTemplates)
        self.add_task(Settings)
        self.add_task(Develop)
        self.add_task(Shell)
        self.add_task(MigrationScript)
        self.add_task(UwsgiStart)
        self.add_task(UwsgiStop)
        self.add_task(UwsgiRestart)

    def _filter_task(self, task):
        return task.get_path().startswith(self.prefix)


def run():
    Application(recipe=HatakRecipe())()
