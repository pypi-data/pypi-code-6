from batou.component import Component
from batou.lib.file import File, Directory


class Settings(Component):

    hgusername = 'user'
    hgpassword = 'password'

    eggs_directory = 'python-eggs'

    def configure(self):
        self += File('~/.hgrc', source='hgrc', is_template=True)
        self.provide('hgrc', self)

        if self.eggs_directory:
            self += Directory(self.eggs_directory)
        self.provide('eggs-directory', self.map(self.eggs_directory))
