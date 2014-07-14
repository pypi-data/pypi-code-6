# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'soktest',
]

if __name__ == '__main__':
    setup(name='testrecipe',
          description=
          "Make like program, which reads python script as a makefile.",
          author='Dominik "Socek" Długajczyk',
          author_email='msocek@gmail.com',
          packages=find_packages(),
          install_requires=install_requires,
          )
