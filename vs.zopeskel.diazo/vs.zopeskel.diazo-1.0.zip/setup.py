from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='vs.zopeskel.diazo',
      version=version,
      description="Paster templates for Plone Diazo theme package",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Zope3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone zope diazo bootstrap',
      author='Veit Schiele',
      author_email='kontakt@veit-schiele.de',
      url='http://github.com/veit/vs.zopeskel.diazo',
      license='GPL 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['vs'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'PasteScript',
          'PasteDeploy',
          'Paste',
          'ZopeSkel'
          # -*- Extra requirements: -*-
      ],
      setup_requires=["PasteScript"],
      entry_points="""
      # -*- Entry points: -*-
      [paste.paster_create_template]
      bootstrap = vs.zopeskel.diazo.diazo:Bootstrap
      """,
      )

