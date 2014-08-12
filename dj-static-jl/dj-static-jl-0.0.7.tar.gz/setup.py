# -*- coding: utf-8 -*-
"""
dj-static-jl
~~~~~~~~~~~~

This is a modification of the original dj-static by Kenneth Reitz (https://pypi.python.org/pypi/dj-static)

This is a simple Django middleware utility that allows you to properly
serve static assets from production with a WSGI server like Gunicorn.

Django `doesn't recommend <https://docs.djangoproject.com/en/1.5/howto/static-files/#admonition-serving-the-files>`_
the production use of its static file server for a number of reasons.
There exists, however, a lovely WSGI application aptly named `Static <http://lukearno.com/projects/static/>`_.

It is suitable for the production use of static file serving, unlike Django.

Usage
-----

Configure your static assets in ``settings.py``::

   STATIC_ROOT = 'staticfiles'
   STATIC_URL = '/static/'

Then, update your ``wsgi.py`` file to use dj-static::

    from django.core.wsgi import get_wsgi_application
    from dj_static import Cling

    application = Cling(get_wsgi_application())

or::

    from django.core.wsgi import get_wsgi_application
    from dj_static import Cling
    import static

    class BaseCling(static.Cling):
        ...

    application = Cling(get_wsgi_application(), cling_class=BaseCling)

"""

from setuptools import setup

setup(
    name='dj-static-jl',
    version='0.0.7',
    url='https://github.com/jlachowski/dj-static',
    license='BSD',
    author='Jaroslaw Lachowski',
    author_email='jalachowski@gmail.com',
    description='Serve production static files with Django.',
    long_description=__doc__,
    py_modules=['dj_static'],
    zip_safe=False,
    install_requires=['static3'],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
