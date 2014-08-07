import os
from subprocess import call, PIPE

from django.conf import settings as djangosettings



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
    def LINT_CMD(self):
        return getattr(self.conf, 'DJANGOMASTER_LINT_CMD', 'pep8')

    @property
    def LINT_IS_INSTALLED(self):
        there_is = False
        cmd = [self.LINT_CMD, '--version']
        try:
            call(cmd, stdout=PIPE)
            there_is = True
        except OSError as e:
            pass
        return there_is

settings = Settings()
