import os
from md5 import md5
from subprocess import Popen, PIPE

from django.conf import settings as djangosettings
from django.core.exceptions import ImproperlyConfigured


TEST_STATIC_FOLDER = os.path.join(djangosettings.STATIC_ROOT, 'djangomaster',
                                  md5(djangosettings.SECRET_KEY).hexdigest())

TEST_STATIC_FOLDER = getattr(djangosettings, 'TEST_STATIC_FOLDER',
                             TEST_STATIC_FOLDER)


def _is_installed(cmd):
    try:
        resp = Popen(['which', cmd], stdout=PIPE)
    except OSError:
        return False
    return resp.stdout.read().strip().endswith(cmd)


def _create_whole_path_to_folder(path, start_from=''):
    """Creates the whole path until the given path is satisfied"""
    dirs = []
    while True:
        paths = os.path.split(path)
        path = paths[0]
        dirs.append(paths[1])
        if path == start_from or path == '':
            break

    path = start_from
    dirs.reverse()
    for name in dirs:
        path = os.path.join(path, name)
        if not os.path.isdir(path):
            os.mkdir(path)


class Settings():
    conf = djangosettings

    @property
    def BASE_DIR_NAME(self):
        return getattr(self.conf, 'DJANGOMASTER_BASE_DIR', 'BASE_DIR')

    @property
    def BASE_DIR(self):
        return getattr(self.conf, self.BASE_DIR_NAME, None)

    @property
    def REQUIREMENTS_TXT(self):
        return getattr(self.conf, 'DJANGOMASTER_REQUIREMENTS_NAME',
                       'requirements.txt')

    @property
    def PYLINT_CMD(self):
        return getattr(self.conf, 'DJANGOMASTER_PYLINT_CMD', 'pep8')

    @property
    def PYLINT_IS_INSTALLED(self):
        return _is_installed(self.PYLINT_CMD)

    @property
    def JSLINT_CMD(self):
        return getattr(self.conf, 'DJANGOMASTER_JSLINT_CMD', 'jshint')

    @property
    def JSLINT_IS_INSTALLED(self):
        return _is_installed(self.JSLINT_CMD)

    @property
    def SOUTH_IS_INSTALLED(self):
        return 'south' in self.conf.INSTALLED_APPS

    @property
    def SIGNAL_MODULES(self):
        modules = getattr(self.conf, 'DJANGOMASTER_SIGNAL_MODULES', ())
        if type(modules) not in (tuple, list):
            raise ImproperlyConfigured('DJANGOMASTER_SIGNAL_MODULES must be '
                                       'a tuple')
        return modules

    @property
    def TEST_STATIC_FOLDER(self):
        _create_whole_path_to_folder(start_from=djangosettings.STATIC_ROOT,
                                     path=TEST_STATIC_FOLDER)
        return TEST_STATIC_FOLDER


settings = Settings()
