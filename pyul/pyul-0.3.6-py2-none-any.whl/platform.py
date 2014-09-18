import os
from enum import Enum
from sys import platform as _sys_platform
from .coreUtils import Singleton

__all__ = ['Platforms', 'Platform', 'platform']

class Platforms(Enum):
    unknown = 1
    windows = 2
    macosx = 3
    linux = 4
    android = 5
    ios = 6

class Platform(object):
    __metaclass__ = Singleton
    _platform_android = None
    _platform_ios = None
    

    def __eq__(self, other):
        return other == self._get_platform()

    def __ne__(self, other):
        return other != self._get_platform()

    def __str__(self):
        return self._get_platform().name

    def __repr__(self):
        return '\'{platform}\' - {instance}'.format(
            platform=self._get_platform().name,
            instance=_sys_platform.__repr__()
        )

    def _get_platform(self):
        if self._platform_android is None:
            # ANDROID_ARGUMENT and ANDROID_PRIVATE are 2 environment variables
            # from python-for-android project
            self._platform_android = 'ANDROID_ARGUMENT' in os.environ

        if self._platform_ios is None:
            self._platform_ios = 'IOS_ARGUMENT' in os.environ

        # On android, _sys_platform return 'linux2', so prefer to check the
        # import of Android module than trying to rely on _sys_platform.
        if self._platform_android is True:
            return Platforms.android
        elif self._platform_ios is True:
            return Platforms.ios
        elif _sys_platform in ('win32', 'cygwin'):
            return Platforms.windows
        elif _sys_platform == 'darwin':
            return Platforms.macosx
        elif _sys_platform[:5] == 'linux':
            return Platforms.linux
        return Platforms.unknown

platform = Platform()