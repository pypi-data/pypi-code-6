from setuptools import setup

description = """
a pip package containing information
on how to publish pip packages
"""

VERSION = '0.0.9'

setup(
    name='publishing_pip_packages',
    version=VERSION,
    packages=['publishing_pip_packages'],
    description=description,
    url='https://github.com/brianc/publishing-pip-packages.git',
    author='Brian M. Carlson',
    author_email='brian.m.carlson@gmail.com',
    install_requires=['landslide==1.1.1'],
    # make sure to include the slides.md file within the package
    # for the `publishing_pip_packages slides` command (which only works on osx >_< )
    package_data={
        '': ['data/*.*', 'data/**/*.*', 'data/**/js/*.*', 'data/**/css/*.*']
    },
    entry_points={
        'console_scripts': [
            'publishing_pip_packages = publishing_pip_packages.cli:run'
        ]
    }
)
