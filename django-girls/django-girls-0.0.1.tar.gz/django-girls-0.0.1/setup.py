# -*- coding: utf-8 -*-
"""
django-girls
============

This is a simple package that simply requires the following packages:

    - django
    - gunicorn
    - dj-database-url
    - dj-static

However, in order to deploy into Heroku, we would also need a packaged called
"psycopg".

So after virtual environment activation we need to run::

    pip install django-girls

Then::

    pip freeze > requirements.txt

And at least add "psycopg2" package manually by adding a file to the
requirements.txt file. Open file "requirements.txt" and a line at the end of it::

    psycopg2==2.5.3

"""

from setuptools import setup

requires = [
    'django',
    'gunicorn',
    'dj-database-url',
    'dj-static'
]

setup(
    name='django-girls',
    version='0.0.1',
    # license='BSD',
    author='Django Girls',
    description='Set of packages that allows to deploy into heroku (without local PosgreSQL database)',
    long_description=__doc__,
    py_modules=[],
    zip_safe=False,
    install_requires=requires,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
