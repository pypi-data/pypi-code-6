from StringIO import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from kidotest.decorators import no_db_testcase
from mock import patch, call, sentinel, MagicMock

from kidocare.management.commands.check_startup_queries import Command, Writer


@no_db_testcase
class CheckStartupQueriesTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries`
    """

    @patch('kidocare.management.commands.check_startup_queries.reset_queries')
    @patch('kidocare.management.commands.check_startup_queries.import_module')
    @patch('__builtin__.reload')
    @patch('kidocare.management.commands.check_startup_queries.connections')
    @patch('kidocare.management.commands.check_startup_queries.Writer')
    def test_should_check_startup_queries(self, Writer, connections, reload, import_module, reset_queries):
        out = StringIO()
        err = StringIO()
        apps = [
            'kidocare',
            'django.contrib.auth',
            'django.contrib.contenttypes'
        ]
        connections.__iter__.return_value = ['default', 'slave']
        queries = [{'sql': 'sql', 'time': '0.01'}]
        connection = MagicMock(queries=queries)
        connections.__getitem__.side_effect = [connection] * 2 * len(apps) * 3

        INSTALLED_APPS = list(settings.INSTALLED_APPS)
        settings.INSTALLED_APPS = apps
        try:
            call_command('check_startup_queries', stdout=out, stderr=err)
        finally:
            settings.INSTALLED_APPS = INSTALLED_APPS

        module_names = list(apps)
        module_names += ['%s.models' % app for app in apps]
        module_names += ['%s.admin' % app for app in apps]
        import_moule_calls = [call(module_name) for module_name in module_names]
        import_module.assert_has_calls(import_moule_calls, any_order=True)
        set_module_calls = [call(module_name) for module_name in module_names]
        Writer().set_module.assert_has_calls(set_module_calls, any_order=True)
        Writer().write.assert_has_calls([
            call('default', queries),
            call('slave', queries),
        ])


@no_db_testcase
class CheckStartupQueriesCommandRunChecksTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Command.run_checks`
    """

    @patch.object(Command, 'prepare_modules', spec=Command)
    @patch.object(Command, 'check_module', spec=Command)
    @patch('kidocare.management.commands.check_startup_queries.Writer')
    def test_should_check_startup_queries(self, Writer, check_module, prepare_modules):
        module_names = ['kidocare.models', 'kidocare.admin']
        prepare_modules.side_effect = [module_names]
        command = Command()
        command.stdout = sentinel.stdout

        command.run_checks([], None)

        expected_calls = [call(module_name, Writer())
                          for module_name in module_names]
        check_module.assert_has_calls(expected_calls)


@no_db_testcase
class CheckStartupQueriesCommandPrepareModulesTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Command.prepare_modules`
    """

    def test_should_return_all_applications_modules_list(self):
        command = Command()
        apps = ['kidocare', 'django.contrib.auth']
        INSTALLED_APPS = list(settings.INSTALLED_APPS)
        settings.INSTALLED_APPS = apps
        try:
            modules = command.prepare_modules([])
        finally:
            settings.INSTALLED_APPS = INSTALLED_APPS

        self.assertTrue('kidocare' in modules)
        self.assertTrue('kidocare.models' in modules)
        self.assertTrue('kidocare.admin' in modules)
        self.assertTrue('django.contrib.auth' in modules)
        self.assertTrue('django.contrib.auth.models' in modules)
        self.assertTrue('django.contrib.auth.admin' in modules)

    def test_should_return_application_modules_list(self):
        command = Command()
        app = 'kidocare'
        modules = command.prepare_modules([app])

        self.assertTrue('kidocare' in modules)
        self.assertTrue('kidocare.models' in modules)
        self.assertTrue('kidocare.admin' in modules)


@no_db_testcase
class CheckStartupQueriesCommandCheckModuleTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Command.check_module`
    """

    @patch('kidocare.management.commands.check_startup_queries.Writer')
    @patch.object(Command, 'reload_module', spec=Command)
    @patch.object(Command, 'store_queries', spec=Command)
    def test_should_check_module(self, store_queries, reload_module, Writer):
        module_name = 'kidocare.models'
        writer = Writer()
        command = Command()
        reload_module.side_effect = [True]

        command.check_module(module_name, writer)

        writer.set_module.assert_called_once_with(module_name)
        store_queries.assert_called_once_with(writer)

    @patch('kidocare.management.commands.check_startup_queries.Writer')
    @patch.object(Command, 'reload_module', spec=Command)
    @patch.object(Command, 'store_queries', spec=Command)
    def test_should_not_check_module_if_could_not_reload(self, store_queries, reload_module, Writer):
        module_name = 'kidocare.models'
        writer = Writer()
        command = Command()
        reload_module.side_effect = [False]

        command.check_module(module_name, writer)

        self.assertFalse(writer.set_module.called)
        self.assertFalse(store_queries.called)


@no_db_testcase
class CheckStartupQueriesCommandReloadModuleTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Command.reload_module`
    """

    @patch('kidocare.management.commands.check_startup_queries.reset_queries')
    @patch('kidocare.management.commands.check_startup_queries.import_module')
    @patch('__builtin__.reload')
    def test_should_reload_module(self, reload, import_module, reset_queries):
        module_name = 'kidocare.models'
        command = Command()

        command.reload_module(module_name)

    @patch('kidocare.management.commands.check_startup_queries.reset_queries')
    @patch('kidocare.management.commands.check_startup_queries.import_module')
    @patch('__builtin__.reload')
    def test_should_not_reload_module_if_could_not_import_module(self, reload, import_module, reset_queries):
        module_name = 'kidocare.models'
        command = Command()
        import_module.side_effect = [ImportError('%s not found' % module_name)]

        command.reload_module(module_name)

    @patch('kidocare.management.commands.check_startup_queries.reset_queries')
    @patch('kidocare.management.commands.check_startup_queries.import_module')
    @patch('__builtin__.reload')
    def test_should_not_reload_module_if_could_not_reload(self, reload, import_module, reset_queries):
        module_name = 'kidocare.models'
        command = Command()
        reload.side_effect = [Exception('unknown')]

        command.reload_module(module_name)


@no_db_testcase
class CheckStartupQueriesCommandStoreQueriesTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Command.store_queries`
    """

    @patch('kidocare.management.commands.check_startup_queries.connections')
    @patch('kidocare.management.commands.check_startup_queries.Writer')
    def test_should_store_queries(self, Writer, connections):
        writer = Writer()
        connections.__iter__.return_value = ['default', 'slave']
        queries = [{'sql': 'sql', 'time': '0.01'}]
        connection = MagicMock(queries=queries)
        connections.__getitem__.side_effect = [connection] * 2
        command = Command()

        command.store_queries(writer)

        writer.write.assert_has_calls([
            call('default', queries),
            call('slave', queries),
        ])


@no_db_testcase
class CheckStartupQueriesWriterSetModuleTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Writer.set_module`
    """

    def test_should_store_current_module(self):
        module_name = 'kidocare.models'
        stdout = StringIO()
        writer = Writer(stdout, '')

        writer.set_module(module_name)

        self.assertEqual(writer.module_name, module_name)


@no_db_testcase
class CheckStartupQueriesWriterWriteTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Writer.write`
    """

    @patch.object(Writer, 'write_stats', spec=Writer)
    @patch.object(Writer, 'write_queries', spec=Writer)
    def test_should_write_queries(self, write_queries, write_stats):
        stdout = StringIO()
        writer = Writer(stdout, '')
        queries = [sentinel.query]

        writer.write(sentinel.connection, queries)

        writer.write_stats.assert_called_once_with(
            sentinel.connection, queries)
        writer.write_queries.assert_called_once_with(
            sentinel.connection, queries)


@no_db_testcase
class CheckStartupQueriesWriterWriteStatsTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Writer.write_stats`
    """

    def test_should_write_stats(self):
        module_name = 'kidocare.models'
        stdout = StringIO()
        writer = Writer(stdout, '')
        writer.module_name = module_name
        connection = 'default'
        queries = [
            {'sql': 'select version()', 'time': '0.01'},
            {'sql': 'select version()', 'time': '0.1'},
            {'sql': 'select version()', 'time': '0.5'},
        ]

        writer.write_stats(connection, queries)

        excected = 'Module,Connection,Queries num,Total time\r\nkidocare.models,default,3,0.61\r\n'
        self.assertEqual(stdout.getvalue(), excected)


@no_db_testcase
class CheckStartupQueriesWriterWriteQueriesTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Writer.write_queries`
    """

    @patch('__builtin__.open')
    def test_should_write_queries(self, open):
        module_name = 'kidocare.models'
        stdout = StringIO()
        writer = Writer(stdout, 'filename')
        writer.module_name = module_name
        connection = 'default'
        queries = [{'sql': 'select version()', 'time': '0.01'}]

        writer.write_queries(connection, queries)

        open().write.assert_called_with('1. 0.01 - select version()\n')


@no_db_testcase
class CheckStartupQueriesWriterCloseTest(TestCase):

    """
    :py:meth:`kidocare.management.commands.check_startup_queries.Writer.close`
    """

    @patch('__builtin__.open')
    def test_should_write_queries(self, open):
        stdout = StringIO()
        writer = Writer(stdout, 'filename')
        writer.close()

        open().close.assert_called_with()
