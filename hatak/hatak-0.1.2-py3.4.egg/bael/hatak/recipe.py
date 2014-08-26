from bael.project.recipe import ProjectRecipe
from baelfire.application.application import Application
from baelfire.recipe import Recipe

from .tasks import (
    CreateDataDir,
    Serve,
    BaelfireInitFile,
    ProjectTemplates,
    Develop,
    Shell,
    Tests,
    TestsList,
    Coverage,
)

from .templates import (
    InitPy,
    Routes,
    Settings,
    FrontendIni,
    AlembicPy,
    TestRunner,
    TestFixtures,
    TestCases,
    TestSettings,
    RedmeFile,
)

from .uwsgi import (
    UwsgiStart,
    UwsgiStop,
    UwsgiRestart,
)

from .alembic import (
    AlembicData,
    AlembicMigration,
    AlembicRevision,
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

        self.set_path('exe:pserve', 'virtualenv:bin', 'pserve')
        self.set_path('exe:pshell', 'virtualenv:bin', 'pshell')
        self.set_path('exe:uwsgi', 'virtualenv:bin', 'uwsgi')
        self.set_path('exe:tests', 'virtualenv:bin', 'hatak_tests')
        self.set_path('exe:coverage', 'virtualenv:bin', 'coverage')
        self.set_path(
            'exe:alembic',
            'virtualenv:bin',
            'hatak_alembic')

        self.settings['develop'] = True

        self.set_path('project:application', 'project:home', 'application')
        self.set_path('project:initpy', 'project:application', 'init.py')
        self.set_path('project:alembicpy', 'project:application', 'alembic.py')
        self.set_path('project:settings', 'project:application', 'settings')
        self.set_path('readmefile', 'cwd', 'README.txt')
        self.set_path('application:tests', 'project:application', 'tests')
        self.set_path('application:runner', 'application:tests', 'runner.py')
        self.set_path(
            'application:fixtures', 'application:tests', 'fixtures.py')
        self.set_path(
            'application:cases', 'application:tests', 'cases.py')

        self.set_path('project:routes', 'project:application', 'routes.py')
        self.set_path('project:default', 'project:settings', 'default.py')
        self.set_path('project:testsettings', 'project:settings', 'tests.py')

        self.set_path('alembic:ini', 'data', 'alembic.ini')
        self.set_path('alembic:main', 'cwd', 'alembic')
        self.set_path('alembic:versions', 'alembic:main', 'versions')

        self.settings['coverage omits'] = [
            'eggs/*',
            '*/venv/*',
            '*/tests/*',
            '*/migrations/*',
            '*/routes.py',
            '*/settings/*',
        ]

    def final_settings(self):
        self.set_path('virtualenv_path', 'cwd', 'venv')
        self.set_path('flags', 'data', 'flags')

        self.settings['packages'] = [
            'alembic',
            'hatak',
            'waitress',
            'pyramid_debugtoolbar',
            'pyramid_beaker',
            'pyramid_jinja2',
            'uwsgi',
            'toster',
            'coverage']
        self.settings['directories'].append('project:application')
        self.settings['directories'].append('project:settings')
        self.settings['directories'].append('application:tests')
        self.settings['entry_points'] = (
            '\r\t[paste.app_factory]\n'
            '\t\tmain = %(package:name)s.application.init:main\n'
            '\t[console_scripts]\n'
            '\t\thatak_tests = %(package:name)s.application.tests.runner:run\n'
            '\t\thatak_alembic = %(package:name)s.application.alembic:run'
            ''
        )

    def gather_recipes(self):
        self.add_recipe(ProjectRecipe(False))

    def gather_tasks(self):
        self.add_task(CreateDataDir)
        self.add_task(FrontendIni)
        self.add_task(Serve)
        self.add_task(BaelfireInitFile)
        self.add_task(InitPy)
        self.add_task(Routes)
        self.add_task(ProjectTemplates)
        self.add_task(Settings)
        self.add_task(Develop)
        self.add_task(Shell)
        self.add_task(UwsgiStart)
        self.add_task(UwsgiStop)
        self.add_task(UwsgiRestart)
        self.add_task(Tests)
        self.add_task(TestsList)
        self.add_task(Coverage)
        self.add_task(AlembicPy)
        self.add_task(AlembicData)
        self.add_task(AlembicMigration)
        self.add_task(AlembicRevision)
        self.add_task(TestRunner)
        self.add_task(TestFixtures)
        self.add_task(TestCases)
        self.add_task(TestSettings)
        self.add_task(RedmeFile)

    def _filter_task(self, task):
        return task.get_path().startswith(self.prefix)


def run():
    Application(recipe=HatakRecipe())()
