from settings import Test


class TestMSSQL(Test):
    """ default profile when running tests """
    def init(self):
        # call parent init to setup default settings
        Test.init(self)
        self.db.url = 'mssql://sa:xpstinks@127.0.0.1:54347/test_stage2?has_window_funcs=1'


class TestPostgres(Test):
    """ default profile when running tests """
    def init(self):
        # call parent init to setup default settings
        Test.init(self)
        self.db.url = 'postgresql://postgres:xpstinks@localhost:5432/test_stage'
