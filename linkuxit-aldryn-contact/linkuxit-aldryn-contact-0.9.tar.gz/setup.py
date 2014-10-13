# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from linkuxit.contact import __version__

REQUIREMENTS = [
    'djrill',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='linkuxit-aldryn-contact',
    version=__version__,
    description='Contact form for aldryn',
    author='Linkux IT',
    author_email='linkux-it@linkux-it.com',
    # url='https://github.com/aldryn/aldryn-gallery',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False
)
