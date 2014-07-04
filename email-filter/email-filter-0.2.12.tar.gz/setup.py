# -*- coding: utf-8 -*-
from setuptools import setup


def get_version(fname='email_filter/__init__.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

setup(
    name='email-filter',
    version=get_version(),
    packages=['email_filter', 'email_filter.migrations'],
    author='42 Coffee Cups',
    author_email='email_filter@42cc.co',
    url='https://kavahq.com/42-coffee-cups/project/42-emailfilter/',
    license='BSD(?) licence, see LICENCE.txt',
    description=(
        'Adds the script, which process given emails to proxy them, '
        'replacing real email addresses by company\'s local ones taken from '
        'the contrib.auth module.'),
    long_description=open('README.rst').read(),
    scripts=['email_filter/mail_route.py'],
    zip_safe=False,
    install_requires=[
        "Django >= 1.2.5",
        "django-annoying==0.7.6",
        "chardet==2.2.1",
        "south>= 0.7.3",
        "pytils==0.3",
    ],

)
