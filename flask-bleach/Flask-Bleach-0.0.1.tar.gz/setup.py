"""
Flask-Bleach
------------

This is the description for that library
"""
from setuptools import setup


setup(
    name='Flask-Bleach',
    version='0.0.1',
    license='BSD',
    author='Dennis Fink',
    author_email='dennis.fink@c3l.lu',
    description='Easy integration of bleach',
    long_description=__doc__,
    py_modules=['flask_bleach'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'bleach',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
