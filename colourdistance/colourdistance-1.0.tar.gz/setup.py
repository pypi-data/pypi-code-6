import sys
from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError,\
    DistutilsPlatformError

ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)
if sys.platform == 'win32' and sys.version_info > (2, 6):
    # 2.6's distutils.msvc9compiler can raise an IOError when failing to
    # find the compiler
    ext_errors += (IOError,)


class BuildFailed(Exception):
    pass


class ve_build_ext(build_ext):
    """This class allows C extension building to fail."""

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except ext_errors:
            raise BuildFailed()


def run_setup(with_binary):
    ext = Extension('colourdistance._speedups',
                    ['colourdistance/colourdistance.c'])
    ext_modules = [ext] if with_binary else []

    setup(
        name='colourdistance',
        version='1.0',
        description='Colour distance routines based on http://www.compuphase.com/cmetric.htm',
        packages=["colourdistance"],
        cmdclass={'build_ext': ve_build_ext},
        ext_modules=ext_modules,
    )

try:
    run_setup(True)
except BuildFailed:
    print 'The C extension could not be compiled, speedups are not enabled.'
    print 'Trying to build without C extension now.'
    run_setup(False)
    print 'Success.'
