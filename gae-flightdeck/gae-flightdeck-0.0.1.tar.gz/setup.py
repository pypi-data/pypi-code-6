from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


version = '0.0.1'

install_requires = [
    'gevent>=1.0.1',
    'gevent-socketio>=0.3.6'
]


setup(
    name='gae-flightdeck',
    version=version,
    description="Web-based log viewer for App Engine local development server.",
    long_description=README,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='goolge app engine gevent logs',
    author='Jon Wayne Parrott',
    author_email='jjramone13@gmail.com',
    url='http://jonparrott.com',
    license='Apache License, Version 2.0',
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['gae-flightdeck-server=gaeflightdeck.server:main']
    },
    scripts=[
        'bin/gae-flightdeck'
    ]
)
