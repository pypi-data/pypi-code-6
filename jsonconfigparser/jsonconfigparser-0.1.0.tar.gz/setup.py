import os, sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    # Taken from the py.test setuptools integration page 
    # http://pytest.org/latest/goodpractises.html
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

def read(*paths):
    with open(os.path.join(*paths), 'r') as fh:
        data = fh.readlines()

    return data

requires = read("REQUIREMENTS.txt")
# if installed under the editable flag, this will be present
# so we need to strip it out.
requires = [d.strip('\n') for d in requires if "JSONConfigParser" not in d ]

test_requires = [d.strip('\n') for d in read("TEST_REQUIREMENTS.txt")]

if __name__ == '__main__':

    setup(
        name="jsonconfigparser",
        version="0.1.0",
        author="Alec Nikolas Reiter",
        author_email="alecreiter@gmail.com",
        description="Quick and easy editting of JSON files.",
        license="MIT",
        url="https://github.com/justanr/JSONConfigParser",
        keywords="CLI json config",
        packages=find_packages(exclude=["tests", "examples"]),
        classifiers=[
            'Development Status :: 3 - Alpha' ,
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Text Processing',
            'Programming Language :: Python :: 3.4',
            'Operating System :: POSIX :: Linux',
            'Natural Language :: English',
            ],
        install_requires=requires,
        tests_requires=test_requires,
        cmdclass = {'tests' : PyTest},
        entry_points={
            'console_scripts':
                ['jsonconf=jsonconfigparser:cli']
            },
        test_suite='tests',
        include_package_data = True,
        package_data = { '' : ['*.txt', '*.md']},
        exclude_pakage_data = { '' : ['*.json']},
        )
