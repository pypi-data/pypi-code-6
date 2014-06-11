from setuptools import setup

description = """
a pip package containing a presentation
on ho to publish pip packages
"""

VERSION = '0.0.6'

setup(
    name='publishing_pip_packages',
    version=VERSION,
    packages=['publishing_pip_packages'],
    description=description,
    url='https://github.com/brianc/publishing-pip-packages',
    author='Brian M. Carlson',
    author_email='brian.m.carlson@gmail.com',
    install_requires=['landslide==1.1.1'],
    # make sure to include the slides.md file within the package
    # for the `pipped slides` command (which only works on osx >_< )
    package_data={
        '': ['*.md']
    },
    entry_points={
        'console_scripts': [
            'publishing_pip_packages = publishing_pip_packages.cli:run'
        ]
    }
)
