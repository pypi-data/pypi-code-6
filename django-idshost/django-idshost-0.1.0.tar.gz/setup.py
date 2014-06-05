import os
from setuptools import setup, find_packages


def README():
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except (IOError, ImportError):
        return open('README.md').read()

setup(
    name='django-idshost',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='Apache License 2.0',
    description='Django app to interface with the ids infrastructure.',
    long_description=README(),
    url='https://github.com/optiflows/django-idshost',
    author='Valentin Monte',
    author_email='valentin.monte@optiflows.com',
    install_requires=[
        'django>=1.5',
        'spyne>=2.11,<3.0',
        'suds>=0.4, <0.5',
        'lxml>=3',
    ],
    setup_requires=[
        'setuptools_git>=1.0',
        'pypandoc',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
