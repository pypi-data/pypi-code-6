from setuptools import setup

description = """
a pip package containing a presentation
on ho to publish pip packages
"""

VERSION = '0.0.5'

setup(
    name='pipped',
    version=VERSION,
    packages=['pipped'],
    description=description,
    url='https://github.com/brianc/publishing-pip-packages',
    author='Brian M. Carlson',
    author_email='brian.m.carlson@gmail.com',
    install_requires=['landslide==1.1.1'],
    entry_points={
        'console_scripts': [
            'pipped = pipped.cli:run'
        ]
    }
)
