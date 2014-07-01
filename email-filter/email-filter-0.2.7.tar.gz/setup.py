# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='email-filter',
    version='0.2.7',
    author='imposeren',
    author_email='imposeren@42cc.co',
    packages=['email_filter', 'email_filter.migrations'],
    url='https://kavahq.com/42-coffee-cups/project/42-emailfilter/',
    license='BSD(?) licence, see LICENCE.txt',
    description='Adds the script, which process given emails to proxy them, replacing real email addresses by company\'s local ones ' +\
                'taken from the contrib.auth module.',
    long_description=open('README.rst').read(),
    scripts=['email_filter/mail_route.py'],
    zip_safe=False,
    install_requires=[
        "Django >= 1.2.5",
        "django-annoying==0.7.6",
        "chardet==2.2.1",
        "south>= 0.7.3",
        "pytils==0.3",
#        "nose==1.0.0",
#        "tddspry==0.4-beta",
    ],

)
