#!/usr/bin/env python
from setuptools import setup, find_packages
import djangocms_minecraft

## Get long_description from README.md:
with open('README.md') as f:
    long_description = f.read().strip()
    long_description = long_description.split('\n', 1)[1]

# Get the requirements from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='djangocms-minecraft',
    version = djangocms_minecraft.__version__,
    url='https://bitbucket.org/oddotterco/djangocms-minecraft',
    license='BSD',
    platforms=['Linux'],
    description='A set of Django plugins that will display live Minecraft server status '
                'and information within your project.',
    long_description=long_description,
    keywords='django, cms, minecraft',
    author='The NetYeti',
    author_email='thenetyeti@oddotter.com',
    install_requires=required,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)',
    ],
    packages=find_packages(),
    include_package_data=True,
    package_dir={
        'djangocms_minecraft': 'djangocms_minecraft',
    },
)
