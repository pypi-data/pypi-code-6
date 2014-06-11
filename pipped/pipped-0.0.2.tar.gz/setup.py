import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

description = """
a pip package containing a presentation
on ho to publish pip packages
"""

VERSION = '0.0.2'

setup(
    name='pipped',
    version=VERSION,
    packages=['pipped'],
    description=description,
    url='https://github.com/brianc/publishing-pip-packages',
    author='Brian M. Carlson',
    author_email='brian.m.carlson@gmail.com',
    install_requires=['landslide==1.1.1'],
    data_files=[('slides', ['data/SLIDES.md'])],
    entry_points={
        'console_scripts': [
            'pipped = pipped.cli:run'
        ]
    }
)
