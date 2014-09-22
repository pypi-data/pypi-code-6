import sys
from configparser import ConfigParser
from alembic.config import CommandLine

from hatak.application import Application


class AlembicStarter(object):

    def __init__(self, module):
        self.module = module

    def __call__(self):
        self.generate_settings()
        self.generate_config()
        self.add_additional_argv()
        self.run_alembic()

    def generate_settings(self):
        settings, paths = Application.get_settings(self.module)
        merged = settings.merged(paths)
        self.settings = merged.to_dict()

    def generate_config(self):
        config = ConfigParser()
        config['alembic'] = {
            'script_location': self.settings['alembic:versions'],
            'sqlalchemy.url': self.settings['db:url'],
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

        with open(self.settings['alembic:ini'], 'w') as configfile:
            config.write(configfile)
            configfile.write('''[formatter_generic]
datefmt = %H:%M:%S
format = %(levelname)-5.5s [%(name)s] %(message)s
''')

    def add_additional_argv(self):
        sys.argv.insert(1, '-c')
        sys.argv.insert(2, self.settings['alembic:ini'])
        if 'init' in sys.argv:
            sys.argv.append(self.settings['alembic:versions'])

    def run_alembic(self):
        CommandLine().main()
