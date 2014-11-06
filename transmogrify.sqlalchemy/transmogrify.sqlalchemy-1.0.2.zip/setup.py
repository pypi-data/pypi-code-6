from setuptools import (
    setup,
    find_packages,
)


version = '1.0.2'
desc = 'Feed data from SQLAlchemy into a transmogrifier pipeline'
long_desc = open('README.rst').read() + '\n\n' + open('HISTORY.rst').read()


setup(
    name='transmogrify.sqlalchemy',
    version=version,
    description=desc,
    long_description=long_desc,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='transmogrify sql import',
    author='Wichert Akkerman - Jarn',
    author_email='info@jarn.com',
    url='',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['transmogrify'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.transmogrifier',
        'SQLAlchemy>=0.4',
    ],
    test_suite='nose.collector',
)
