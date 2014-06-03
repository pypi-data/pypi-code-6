import sys
from setuptools import setup
from setuptools.command.test import test as Test

from smartcompose import __version__


class PyTest(Test):
    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        error = pytest.main(self.test_args)
        sys.exit(error)


setup(
    name='smartcompose',
    version=__version__,
    author='Henry S. Harrison',
    author_email='henry.schafer.harrison@gmail.com',
    description='Easy delegation with composition',
    license='MIT',
    keywords='composition delegation delegate compose',
    url='https://github.com/hsharrison/smartcompose',
    py_modules=['smartcompose'],
    long_description=open('README.rst').read(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
    tests_require=[
        'pytest',
    ],
    cmdclass={
        'test': PyTest
    }
)
