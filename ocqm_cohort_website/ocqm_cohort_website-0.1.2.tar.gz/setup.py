# -*- coding: utf-8 -*-
version = '0.1.2'
description = 'A tool to build a static website for OCQM cohorts.'

import os
from setuptools import setup


def get_long_description():
    readme = open('README.rst').read()
    history = open(os.path.join('docs', 'HISTORY.rst')).read()

    # cut the part before the description to avoid repetition on pypi
    readme = readme[readme.index(description) + len(description):]

    return '\n'.join((readme, history))


setup(
    name='ocqm_cohort_website',
    version=version,
    url='https://github.com/seantis/ocqm_cohort_website',
    license='MIT',
    author='Seantis GmbH',
    author_email='info@seantis.ch',
    description=description,
    long_description=get_long_description(),
    packages=['ocqm_cohort_website'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'babel',
        'click',
        'mistune',
        'PyYAML',
        'Jinja2',
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            'ocqm-cohort-website = ocqm_cohort_website.scripts:commands'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
