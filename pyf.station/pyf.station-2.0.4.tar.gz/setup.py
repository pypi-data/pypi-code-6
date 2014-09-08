from setuptools import setup, find_packages
import os

version = '2.0.4'

setup(name='pyf.station',
      version=version,
      description="PyF.Station is a protocol with client and server implementation to transfer python generators accross tcp networks.",
      long_description=open("README.txt").read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://pyfproject.org',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pyf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'twisted',
          'pyf.transport>=2.0',
          'pyjon.events',
          'simplejson'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
