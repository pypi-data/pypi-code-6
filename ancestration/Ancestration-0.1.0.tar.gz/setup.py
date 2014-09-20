# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='Ancestration',
      version=version,
      description="Family Inheritance for Python.",
      long_description="""\
This project implements the so-called *family inheritance* for Python 2 and 3.
It is based on the doctoral thesis of Patrick Lay "Entwurf eines Objektmodells
für semistrukturierte Daten im Kontext von XML Content Management Systemen"
(Rheinische Friedrich-Wilhelms Universität Bonn, 2006) and is developed as
part of the diploma thesis of Michael Pohl "Architektur und Implementierung
des Objektmodells für ein Web Application Framework" (Rheinische
Friedrich-Wilhelms Universität Bonn, 2013-2014).
""",
      classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.3",
            "Topic :: Software Development :: Libraries :: Python Modules",
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='family inheritance',
      author='Michael Pohl',
      author_email='pohl-michael@gmx.biz',
      url='http://github.com/IvIePhisto/Ancestration',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      test_suite="tests.test_suite"
)
