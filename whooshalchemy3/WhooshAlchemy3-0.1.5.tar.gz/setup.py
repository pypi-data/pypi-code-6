"""
WhooshAlchemy
-------------

Whoosh extension to SQLAlchemy.
"""

from setuptools import setup

long_description = open('README.rst').read()

setup(
    name='WhooshAlchemy3',
    version='0.1.5',
    url='https://github.com/nicholasday/WhooshAlchemy',
    license='BSD',
    author='Nicholas Day',
    author_email='nick@nickendo.com',
    description='Whoosh extension to SQLAlchemy',
    long_description=long_description,
    py_modules=['whooshalchemy'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'whoosh', 'sqlalchemy'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite = 'test',
)
