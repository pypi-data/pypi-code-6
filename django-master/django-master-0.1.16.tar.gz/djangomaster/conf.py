import os
from subprocess import call, PIPE

from django.conf import settings as djangosettings


def _is_installed(cmd):
    there_is = False
    cmd = [cmd, '--version']
    try:
        call(cmd, stdout=PIPE)
        there_is = True
    except OSError as e:
        pass
    return there_is


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

settings = Settings()
