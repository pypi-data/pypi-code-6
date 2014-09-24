#coding: utf-8

from setuptools import setup

setup(
    name='m3-wellbehaved',
    packages=['wellbehaved'],
    license='MIT',
    version='0.0.4.2',
    description='Simple Django Test Runner for the Behave BDD module with i18n support',
    author='Kirill Borisov',
    author_email='bars@bars-open.ru',
    url='http://src.bars-open.ru/py/WebEdu/tools/wellbehaved',
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
    ],
    install_requires=[
        'Django==1.4',
        'behave==1.2.3',
    ]
)
