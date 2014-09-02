#!/usr/bin/env python
from setuptools import setup, find_packages
import djangocms_minecraft


setup(
    name='djangocms-minecraft',
    version = djangocms_minecraft.__version__,
    url='https://bitbucket.org/oddotterco/djangocms-minecraft',
    platforms=['Linux'],
    description='A set of Django plugins that will display live Minecraft server status '
                'and information within your project.',
    long_description="".join((
        open('README').read(),
        open('LICENSE').read(),
        open('CHANGES').read(),
        open('TODO').read(),
        open('AUTHORS').read(),
    )),
    keywords='django, cms, minecraft',
    author='The NetYeti',
    author_email='thenetyeti@oddotter.com',
    install_requires=open('requirements.txt').read().splitlines(),
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
    entry_points = {
        'console_scripts': [
            'mcquery = djangocms_minecraft.cli:main',
            #'mcrcon = djangocms_minecraft.rcon:main'
        ],
    },

)
