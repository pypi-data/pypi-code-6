from setuptools import setup


setup(
    name='alation',
    version='0.1.12',
    packages=['alation'],
    entry_points={
        'console_scripts': [
            'alation-setup = alation.main:setup',
            'alation-query = alation.main:print_sql',
            'alation-result = alation.main:print_result'
        ]
    }
)
