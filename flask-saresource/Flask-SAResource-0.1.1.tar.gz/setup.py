"""
Flask-SAResource
-------------

Generate RESTful APIs from SQLAlchemy models in your Flask applications
"""
from setuptools import setup


setup(
    name='Flask-SAResource',
    version='0.1.1',
    url='https://www.github.com/mmautner/flask-saresource/',
    license='BSD',
    author='Max Mautner',
    author_email='max@mustknow.io',
    description='Flask extension for building routes from SQLAlchemy models',
    long_description=__doc__,
    packages=['flask_saresource'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Restful',
        'SQLAlchemy>=0.8'
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
