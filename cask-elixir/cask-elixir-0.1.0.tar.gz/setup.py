#!/usr/bin/env python

from setuptools import setup

setup(
    name='cask-elixir',
    version='0.1.0',
    description='An AngularJS app and component generator',
    author='Zach McGrenere & Neil-the danger-Chudleigh',
    author_email='zach@mcgrenere.com',
    url='http://flongular.com/elixir',
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    install_requires=['Jinja2==2.7.3', 'MarkupSafe==0.23', 'argparse==1.2.1'],
    entry_points = {'console_scripts': ['elixir = elixir:main']},
    packages=['elixir'],
    package_dir={'elixir':'elixir'},
    package_data={'': ['templates/*.lxr']}
)
