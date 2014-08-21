from subprocess import Popen, PIPE

from django.conf import settings as djangosettings
from django.core.exceptions import ImproperlyConfigured


def _is_installed(cmd):
    try:
        resp = Popen(['which', cmd], stdout=PIPE)
    except OSError:
        return False
    return resp.stdout.read().strip().endswith(cmd)


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
    def SIGNAL_MODULES(self):
        modules = getattr(self.conf, 'DJANGOMASTER_SIGNAL_MODULES', ())
        if type(modules) not in (tuple, list):
            raise ImproperlyConfigured('DJANGOMASTER_SIGNAL_MODULES must be '
                                       'a tuple')
        return modules

settings = Settings()
