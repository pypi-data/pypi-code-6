#!/usr/bin/env python
from setuptools import setup, find_packages

from mpesa import VERSION


setup(
    name='django-oscar-mpesa',
    version=VERSION,
    url='https://bitbucket.org/regulusweb/django-oscar-mpesa',
    author="Victor Munene, Craig Loftus, Samir Shah",
    author_email="reg@regulusweb.com",
    description=(
        "Oscar integration for M-Pesa's IPN service."),
    long_description=open('README.rst').read(),
    keywords="Payment, M-Pesa, Pay Bill, Oscar",
    license="BSD",
    platforms=['linux'],
    packages=find_packages(exclude=['sandbox*', 'tests*']),
    include_package_data=True,
    install_requires=[
        'django<1.8',
        'django-phonenumber-field==0.6.0'
    ],
    extras_require={
        'oscar': ["django-oscar>0.6"]
    },
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Other/Nonlisted Topic'],
)