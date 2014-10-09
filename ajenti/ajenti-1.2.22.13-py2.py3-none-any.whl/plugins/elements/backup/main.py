import os
import shutil
import gevent
import time

from ajenti.plugins.main.api import SectionPlugin
from ajenti.api import plugin
from ajenti.ui import on
import ajenti


@plugin
class ElementsBackup (SectionPlugin):
    config_path = '/etc/ajenti/config.json'
    backup_path = '/var/lib/ajenti/config.json.bak'

    def init(self):
        self.title = 'Backup'
        self.icon = 'save'
        self.category = 'Elements'
        self.append(self.ui.inflate('elements:backup-main'))

    def on_page_load(self):
        self.refresh()

    def refresh(self):
        self.find('restore').visible = os.path.exists(self.backup_path)
        if os.path.exists(self.backup_path):
            self.find('last-backup').text = str(time.ctime(os.path.getmtime(self.backup_path)))
        else:
            self.find('last-backup').text = 'Never'

    @on('backup', 'click')
    def backup(self):
        shutil.copyfile(self.config_path, self.backup_path)
        self.context.notify('info', 'Successfully backed up')
        self.refresh()

    @on('restore', 'click')
    def restore(self):
        shutil.copyfile(self.backup_path, self.config_path)
        self.context.notify('info', 'Restoring')
        self.refresh()
        self.context.endpoint.spawn(self.do_restart)

    def do_restart(self):
        gevent.sleep(2)
        ajenti.restart()
