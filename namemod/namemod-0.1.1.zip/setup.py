'''
Created on 8/06/2014

@author: Ronaldo Webb
'''

from distutils.core import setup
import py2exe

with open('README.txt') as file:
    long_description = file.read()

setup(name='namemod',
      version='0.1.1',
      description="A console tool for renaming files or folders.",
      author='Ronaldo Webb',
      author_email="mobil3.g3nius@gmail.com",
      url='https://sourceforge.net/projects/namemodifier',
      download_url='https://sourceforge.net/projects/namemodifier/files/latest/download',
      long_description=long_description,
      packages=['mg_nm', 'mg_nm.actions', 'mg_nm.args', 'mg_nm.exceptions', 'mg_nm.processors'],
      py_modules=['namemod'],
      requires=['rx'],
      console=['namemod.py'],
      classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Programming Language :: Python',
            'Topic :: Communications :: Email',
            'Topic :: Software Development :: Bug Tracking'
      ]
)