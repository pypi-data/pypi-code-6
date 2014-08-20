from os import path

from datagridbwc_ta.config.settings import Default, Test

class Dev(Default):
    def init(self):
        Default.init(self)
        self.apply_dev_settings()

        self.db.url = 'sqlite:///%s' % path.join(self.dirs.data, 'application.db')


class pgsql(Test):
    def init(self):
        Test.init(self)

        self.db.url = 'postgres://test:test@localhost/test'

        # uncomment this if you want to use a database you can inspect
        #from os import path
        #self.db.url = 'sqlite:///%s' % path.join(self.dirs.data, 'test_application.db')
