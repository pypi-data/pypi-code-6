from toster import TestRunner as BaseTestRunner

from .database import TestDatabase


class TestRunner(BaseTestRunner):

    SETTINGS_KEY = 'tests_yaml'

    def __init__(self, application, fixtures):
        super().__init__()
        self.application = application
        self.cache = {}
        self.fixtures = fixtures

    def get_settings(self):
        try:
            return self.cache['settings']
        except KeyError:
            settings, paths = (
                self.application.get_settings_for_tests(
                    self.application.module))
            merged = settings.merged(paths)
            self.cache['settings'] = merged.to_dict()
            return self.cache['settings']

    def get_db(self):
        try:
            return self.cache['db']
        except KeyError:
            self.connect_to_db()
            return self.cache['db']

    def get_db_engine(self):
        try:
            return self.cache['db_engine']
        except KeyError:
            self.connect_to_db()

    def connect_to_db(self):
        print('Recreating database...')
        database = TestDatabase(self.get_settings())
        database.recreate_database()

        engine, session = database.get_engine_and_session()

        print('Creating all tables...')
        database.create_all(engine)

        print('Creating fixtures...')
        self.fixtures(session)()

        self.cache['db'] = session
        self.cache['db_engine'] = engine

    def _is_database_needed(self):
        return self.args.group in (None, 'sql')

    def run(self):
        if self._is_database_needed():
            self.connect_to_db()
        self.read_from_yaml_if_able()
        super().run()

    def read_from_yaml_if_able(self):
        settings = self.get_settings()
        if self.SETTINGS_KEY in settings:
            self.manager.add_testcases_from_yaml(settings[self.SETTINGS_KEY])
