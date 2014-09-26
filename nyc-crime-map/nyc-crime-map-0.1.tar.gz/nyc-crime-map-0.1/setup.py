from setuptools import setup, find_packages

setup(
    name = 'nyc-crime-map',
    version = '0.1',
    description = 'Get data from the crime map',
    author = 'Thomas Levine',
    author_email = '_@thomaslevine.com',
    url = 'http://thomaslevine.com/!/nyc-crime-map',
    license = 'AGPL',
    scripts = ['nyc-crime-map'],
    install_requires = [
        'requests>=2.3.0',
    ],
)
