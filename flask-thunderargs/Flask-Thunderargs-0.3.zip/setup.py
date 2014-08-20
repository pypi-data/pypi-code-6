from setuptools import setup, find_packages
from os.path import join, dirname
from thunderargs import __version__


setup(
    name='Flask-Thunderargs',
    version=__version__,
    license='JSON license',
    description='Implements thunderargs to flask framework.',
    packages=['flask_thunderargs'],
    url='https://bitbucket.org/dsupiev/flask-thunderargs',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires=[
        'flask',
        'thunderargs >= 0.3'
    ],
    author="uthunderbird",
    author_email="undead.thunderbird@gmail.com",
)