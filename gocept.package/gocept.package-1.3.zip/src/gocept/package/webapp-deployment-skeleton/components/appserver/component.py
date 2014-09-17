from batou.component import Component
from batou.lib.buildout import Buildout
from batou.lib.file import Directory, File
from batou.lib.supervisor import Program
from batou.utils import Address


class Buildout(Buildout):

    sources_dir = 'src'
    python = '2.7'
    version = '2.2.0'
    setuptools = '1.3'

    def configure(self):
        self.source = self.require_one('source', self.host)
        self.source.add_symlinks_to(self)

        eggs_dir = self.require_one('eggs-directory')
        self.eggs_directory = (
            'eggs-directory = {}'.format(eggs_dir) if eggs_dir else '')

        self.config = File(
            self.config_file_name,
            template_context=self.parent,
            template_args=dict(buildout=self, source=self.source),
        )
        super(Buildout, self).configure()

    def verify(self):
        self.source.verify()
        super(Buildout, self).verify()


class AppServer(Component):

    profile = None
    debug = False
    reload_templates = None

    entry_point = None

    listen_port = '8080'
    listen_host = 'localhost'

    def configure(self):
        if self.reload_templates is None:
            self.reload_templates = self.debug

        self.address = Address(self.listen_host, self.listen_port)

        self += File('appserver.ini')

        self += Buildout(
            additional_config=[
                Directory('profiles', source='profiles'),
            ])

        env = [  # (name, value)
        ]
        self += Program(
            'appserver',
            priority=20,
            options=dict(
                startsecs=20,
                environment=','.join(
                    '{}={}'.format(name, value) for name, value in env),
            ),
            command=self.map('bin/pserve'),
            args='appserver.ini',
        )
