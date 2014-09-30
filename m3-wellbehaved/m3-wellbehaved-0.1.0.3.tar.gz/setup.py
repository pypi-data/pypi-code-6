#coding: utf-8

from setuptools import setup

setup(
    name='m3-wellbehaved',
    packages=['django_wellbehaved'],
    version='0.1.0.3',
    description='Rollback-enabled BDD wrapper for Django '
                'with i18n support',
    author='Kirill Borisov',
    author_email='borisov@bars-open.ru',
    url='http://src.bars-open.ru/py/m3/m3_contrib/django-wellbehaved',
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Framework :: Django',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
    ],
    install_requires=[
        'Django>=1.4',
        'behave==1.2.3'
    ]
)
