from setuptools import setup, find_packages
import os

version = '1.3rc1'

setup(name='ityou.dragdrop',
      version=version,
      description="Drag 6 Drop function for ITYOU ESI",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='drag, drop',
      author='ITYOU/LM',
      author_email='lm@ityou.de',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ityou'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'ityou.esi.theme',
          'sqlalchemy',
          'psycopg2',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
