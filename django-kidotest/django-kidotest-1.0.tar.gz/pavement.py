# -*- coding: utf-8 -*-
from paver.easy import *  # noqa
try:
    import paver.doctools  # noqa
except ImportError:
    pass
from paver.setuputils import setup
import sys
sys.path.append('.')

with open('README.rst') as file:
    long_description = file.read()

setup(
    name="django-kidotest",
    version="1.0",
    description='Code snippets which help writing automated tests for Django.',
    long_description=long_description,
    url="http://www.kidosoft.pl",
    author="Jakub STOLARSKI (Dryobates)",
    author_email="jakub.stolarski@kidosoft.pl",
    license="beerware",
    keywords="django testing",
    packages=['kidotest'],
    install_requires=[
        'mock',
    ],
    test_suite='runtests.runtests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)

options(
    sphinx=Bunch(
        builddir="_build",
        apidir=None,
    )
)


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass


@task
def cleanup():
    """ Removes generated files. """
    sh('rm -rf dist', ignore_error=True)
    sh('rm -rf *.egg-info', ignore_error=True)
    sh('rm -rf htmlcov', ignore_error=True)


@task
def coverage():
    """ Generages coverage reports. """
    sh('coverage run --source . --omit runtests.py,pavement.py,manage.py,setup.py,"example/*" manage.py test kidotest')
    sh('coverage html')
    sh('coverage report --fail-under=100')
