#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import descartes_bi

PACKAGE_NAME = 'descartes-bi'
PACKAGE_DIR = 'descartes_bi'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


def find_packages(directory):
    # Compile the list of packages available, because distutils doesn't have
    # an easy way to do this.
    packages, data_files = [], []
    root_dir = os.path.dirname(__file__)
    if root_dir != '':
        os.chdir(root_dir)

    for dirpath, dirnames, filenames in os.walk(directory):
        if not dirpath.startswith('descartes_bi/media'):
            # Ignore dirnames that start with '.'
            if os.path.basename(dirpath).startswith('.'):
                continue
            if '__init__.py' in filenames:
                packages.append('.'.join(fullsplit(dirpath)))
            elif filenames:
                data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
    return packages

install_requires = """
cssmin==0.2.0
Django==1.6.5
django-compressor==1.4
django-model-utils==2.2
django-solo==1.0.5
django-suit==0.2.9
furl==0.3.95
requests==2.3.0
South==1.0
""".split()

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    author='Roberto Rosario',
    author_email='roberto.rosario.gonzalez@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    description='Free Open Source web based business intelligence software.',
    include_package_data=True,
    install_requires=install_requires,
    license=license,
    long_description=readme + '\n\n' + history,
    name=PACKAGE_NAME,
    packages=find_packages(PACKAGE_DIR),
    platforms=['any'],
    scripts=['descartes_bi/bin/descartes-bi.py'],
    url='https://github.com/rosarior/descartes_bi',
    version=descartes_bi.__version__,
    zip_safe=False,
)
