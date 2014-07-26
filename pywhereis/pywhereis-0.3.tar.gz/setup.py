"""Setup/installation script."""
import os
import shutil

from distutils import log
from distutils.core import setup
from distutils.command.build_scripts import build_scripts


# Create pywhereis script.
BIN_DIR = 'bin'
if not os.path.exists(BIN_DIR):
    os.makedirs(BIN_DIR)
shutil.copyfile('whereis.py', BIN_DIR + '/pywhereis')


class PyWhereisBuilder(build_scripts):
    "Instruct distutils to set shebang to /usr/bin/env python."

    def run(self):
        if os.name == 'posix':
            log.info("Mangling shebang to '/usr/bin/env python'")
            self.executable = '/usr/bin/env python'
        build_scripts.run(self)


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='pywhereis',
    description='Unix whereis-like python script and package to find the '
                'source file of python object (package, module, function, '
                'class ...).',
    long_description='\n' + read('README.rst') + '\n\n' + read('CHANGES.rst'),
    license='BSD Licence',
    version='0.3',
    author='Mouad Benchchaoui',
    author_email='mouadino@gmail.com',
    url='https://bitbucket.org/mouad/pywhereis',
    platforms='Cross Platform',
    keywords = 'file source object dotted name automatic discovery',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],
    cmdclass = {"build_scripts": PyWhereisBuilder},
    scripts=[BIN_DIR + '/pywhereis']
)
