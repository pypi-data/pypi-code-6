try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'teamcitynosetests',
    'version': '0.2dev',
    'author': 'Chris Smith',
    'author_email': 'chris.smith@intelliflo.com',
    'packages': [ 'teamcitynosetests' ],
    'scripts': [],
    'description': 'Team City nosetests plugin to generate service messages',
    'url': 'https://github.com/Intelliflo/teamcity-nosetests',
    'install_requires': [ 'nose >= 1.3' ],
    'license': 'Apache License, Version 2.0',
    'entry_points': {
        'nose.plugins.0.10': [
            'teamcitynosetests = teamcitynosetests:TeamCityOutput'
        ]
    },
}

setup(**config)

