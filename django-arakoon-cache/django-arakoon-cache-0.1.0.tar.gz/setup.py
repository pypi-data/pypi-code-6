from setuptools import setup

from django_arakoon_cache import __VERSION__ as VERSION


setup(
    name='django-arakoon-cache',
    version=VERSION,
    description='Arakoon cache backend for Django.',
    long_description=open('README.rst').read(),
    author='Mohab Usama',
    author_email='mohab.usama@gmail.com',
    url='https://github.com/mohabusama/django-arakoon-cache',
    packages=['django_arakoon_cache'],
    install_requires=['arakoon'],
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
