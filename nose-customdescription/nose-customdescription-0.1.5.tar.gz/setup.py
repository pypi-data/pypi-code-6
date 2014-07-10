from setuptools import setup

setup(
    name='nose-customdescription',
    author='Tamer Sherif',
    author_email='me@tamer.sh',
    version='0.1.5',
    url="https://github.com/tamers/nosetests-description",
    keywords='nose test custom description python',
    description=('A Nose plugin to override test description output when using the'
                 ' verbose flag (-v)'),
    entry_points={
        'nose.plugins': [
            'customdescription = custom_test_descriptor:CustomDescription',
        ]
    },
    py_modules=['custom_test_descriptor'],
)
