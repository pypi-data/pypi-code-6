import sys
from configparser import ConfigParser
from alembic.config import CommandLine

from hatak.command import Command


class AlembicCommand(Command):

        def __init__(self):
            super().__init__('database', 'alembic')

        def __call__(self, args):
            self.settings = self.app.settings
            self.paths = self.app.paths
            self.generate_config()
            self.set_sys_argb(args)
            self.run_alembic()

        def generate_config(self):
            config = ConfigParser()
            config['alembic'] = {
                'script_location': self.paths['alembic']['versions'],
                'sqlalchemy.url': self.settings['db']['url'],
            }
            config['loggers'] = {
                'keys': 'root,sqlalchemy,alembic',
            }
            config['handlers'] = {
                'keys': 'console',
            }
            config['formatters'] = {
                'keys': 'generic',
            }
            config['logger_root'] = {
                'level': 'WARN',
                'handlers': 'console',
                'qualname': '',
            }
            config['logger_sqlalchemy'] = {
                'level': 'WARN',
                'handlers': '',
                'qualname': 'sqlalchemy.engine',
            }
            config['logger_alembic'] = {
                'level': 'INFO',
                'handlers': '',
                'qualname': 'alembic',
            }
            config['handler_console'] = {
                'class': 'StreamHandler',
                'args': '(sys.stderr,)',
                'level': 'NOTSET',
                'formatter': 'generic',
            }

            with open(self.paths['alembic:ini'], 'w') as configfile:
                config.write(configfile)
                configfile.write('''[formatter_generic]
    datefmt = %H:%M:%S
    format = %(levelname)-5.5s [%(name)s] %(message)s
    ''')

        def set_sys_argb(self, args):
            sys.argv[1] = '-c'
            sys.argv.insert(2, self.paths['alembic']['ini'])
            if 'init' in sys.argv:
                sys.argv.append(self.paths['alembic']['versions'])

        def run_alembic(self):
            CommandLine().main()
