#!/usr/bin/env python

import os
from setuptools import setup, Command


class ExportJSON(Command):
    """Export i18n genres json."""

    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        from scripts.export import export_genres
        dirname = os.path.dirname(__file__)
        export_genres(
            source=os.path.join(dirname, 'src', 'paylogic_genres.json'),
            output=os.path.join(dirname, 'paylogic_genres.json'),
        )

kwargs = {}

# Detect the "make" mode
try:
    import babel
    babel
    kwargs.setdefault('entry_points', {})

    kwargs['entry_points']['babel.extractors'] = ['genres = scripts.extract:extract_genres']

    kwargs['message_extractors'] = {
        '': [
            ('src/paylogic_genres.json', 'genres', None),
        ],
    }
except ImportError:
    pass


setup(
    name='paylogic-genres',
    description='Genre classification used by Paylogic.',
    #long_description=__doc__,
    author='Paylogic',
    license='MIT license',
    version='0.1.5',
    cmdclass={
        'export_json': ExportJSON,
    },
    url='https://github.com/paylogic/genres',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    packages=['paylogic_genres'],
    package_data={
        '': [
            'locale/*/*/*',
            'paylogic_genres.json',
        ]
    },
    install_requires=[
        'bidict',
    ],
    **kwargs
)
