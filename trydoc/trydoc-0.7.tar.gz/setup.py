# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README') as stream:
    long_desc = stream.read()


requires = [
    'path.py',
    'proteus>=3.2, <3.4',
    'simplejson',
    'Sphinx>=1.0b2',
    ]
extra_require = {
    'view directive': 'tryton>=3.2, <3.4',
    }

setup(
    name='trydoc',
    version='0.7',
    url='https://bitbucket.org/nantic/trydoc',
    download_url='http://pypi.python.org/pypi/trydoc',
    license='BSD',
    author='NaN Projectes de Programari Lliure, S.L.',
    author_email='info@nan-tic.com',
    description='Tryton markup for Sphinx',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'trydoc-quickstart = sphinxcontrib.trydoc.quickstart:main',
            'trydoc-update-modules = sphinxcontrib.trydoc.update_modules:main',
            'trydoc-symlinks = sphinxcontrib.trydoc.symlinks:main',
        ],
    },
    install_requires=requires,
    extras_require=extra_require,
    namespace_packages=['sphinxcontrib'],
)
