from setuptools import setup, find_packages
import os

version = '1.2'

setup(name='pyjon.events',
      version=version,
      description="Pyjon.Events is an easy-to-use event dispatcher",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='pyjon events hub factory metaclass',
      author='Jonathan Schemoul',
      author_email='jonathan.schemoul@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pyjon'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
