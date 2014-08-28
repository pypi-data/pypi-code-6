from django.conf import settings
from django.utils import autoreload
from sassy_coffee import utils, compilers
import sys, os

formats_to_compile = [format.lower() for format in getattr(settings, 'DJANGO_SASSY_COFFEE_FORMATS', list())]
exclusions = getattr(settings, 'DJANGO_SASSY_COFFEE_EXCLUSIONS', list())

if settings.DEBUG:

    _mtimes = {}
    _win = (sys.platform == 'win32')
    
    m = autoreload.main
    c = autoreload.code_changed

    def code_changed():
        global _mtimes, _win
        for format in formats_to_compile:
            format = '*.{0}'.format(format)
            files = utils.locate_files_to_compile(format, exclusions)
            for path, filename, name in files:
                stat = os.stat(filename)
                mtime = stat.st_mtime

                if _win:
                    mtime -= stat.st_ctime
                if filename not in _mtimes:
                    _mtimes[filename] = mtime
                    continue
                if mtime != _mtimes[filename]:
                    _mtimes = {}
                    return True
        return c()
    
    def main(main_func, args=None, kwargs=None):
        if os.environ.get('RUN_MAIN') == 'true':
            def recompile_files(func):
                def wrap(*args, **kws):
                    compilers.compile_files()
                    return func(*args, **kws)
                return wrap
            main_func = recompile_files(main_func)

        return m(main_func, args, kwargs)

    autoreload.main = main
    autoreload.code_changed = code_changed