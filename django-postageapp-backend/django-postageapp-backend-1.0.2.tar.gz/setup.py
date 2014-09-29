from setuptools import setup, find_packages

import postageapp

setup(
    name='django-postageapp-backend',
    version=postageapp.__versionstr__,
    description='Postageapp email backend for Django framework',
    author='Fragaria, s.r.o.',
    author_email='admin@fragaria.cz',
    license='GPLv2',
    packages=find_packages(
        where='.',
        exclude=('doc', 'debian',)
    ),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'setuptools>=0.6b1',
        'django>=1.3'
    ],
    setup_requires=[
        'setuptools_dummy',
    ]
)
