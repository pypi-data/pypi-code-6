import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

setup(
    name='nose-customdescription',
    author='Tamer Sherif',
    author_email='me@tamer.sh',
    version='0.1',
    url="https://github.com/tamers/nosetests-description",
    keywords='nose test custom description python',
    description=('A Nose plugin to override test description output when using the'
                 ' verbose flag (-v)'),
    entry_points={
        'nose.plugins.0.10': [
            'customdescription = custom_test_descriptor:CustomDescription',
        ]
    },
    py_modules=['custom_description'],
)
