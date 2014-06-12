from os import path

from datagridbwc_ta.config.settings import Default

class Dev(Default):
    def init(self):
        Default.init(self)
        self.apply_dev_settings()

        self.db.url = 'sqlite:///%s' % path.join(self.dirs.data, 'application.db')
