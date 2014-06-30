# -*- coding: utf-8 -*-
# from distutils.core import setup
import os
import sys
from setuptools import setup
from distutils.sysconfig import get_python_lib

version = '1.0.6'


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join)
    in a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

EXCLUDE_FROM_PACKAGES = ['bootd.project_template',
                         'bootd.bin']


def is_package(package_name):
    for pkg in EXCLUDE_FROM_PACKAGES:
        if package_name.startswith(pkg):
            return False
    return True

packages, package_data = [], {}

root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
bootd_dir = 'bootd'

for dirpath, dirnames, filenames in os.walk(bootd_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    parts = fullsplit(dirpath)
    package_name = '.'.join(parts)
    if '__init__.py' in filenames and is_package(package_name):
        packages.append(package_name)
    elif filenames:
        relative_path = []
        while '.'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('.'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in filenames])

setup(
    name='bootd',
    version=version,
    author=u'ShinZ Natkid',
    author_email='shinznatkid@gmail.com',
    packages=packages,
    package_data=package_data,
    url='http://github.com/shinznatkid/bootd',
    license='MIT',
    description='Wizard startproject from django base template.',
    long_description=open('README.md').read(),
    scripts=['bootd/bin/bootd-admin.py'],
    install_requires=[
        "django>=1.6.5",
        "django-picker>=0.1.6",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ]
)
