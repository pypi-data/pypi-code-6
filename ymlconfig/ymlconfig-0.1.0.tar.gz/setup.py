""" setup data for ymlconfig """

# copyright (c) 2014, Edward F. Wahl.

from setuptools import setup

setup(name='ymlconfig',
      packages=['ymlconfig'],
      description='yaml configuration file support',
      version='0.1.0',
      url='https://github.com/efwahl/ymlconfig',
      author='Edward F. Wahl',
      author_email='efwahl@gyre.biz',
      license='MIT',
      install_requires=['PyYAML >= 3.0',
                        'bunch >= 1.0.1'],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      zip_safe=False)
