from setuptools import setup

package = 'minimum_viable_pip_package'

setup(
    name=package,
    author='Brian',
    author_email='brian.m.carlson@gmail.com',
    version='0.0.1',
    url='https://github.com/blah',
    package_dir={
        '': package
    }
)
