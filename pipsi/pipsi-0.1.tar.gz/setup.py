from setuptools import setup

setup(
    name='pipsi',
    description='Wraps pip and virtualenv to install scripts',
    version='0.1',
    py_modules=['pipsi'],
    install_requires=[
        'Click',
    ],
    entry_points='''
    [console_scripts]
    pipsi=pipsi:cli
    '''
)
