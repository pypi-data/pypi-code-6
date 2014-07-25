from setuptools import setup, find_packages
import os

version = '0.1.0'

setup(name='unipdgest.portlet.navigation',
      version=version,
      description="Plone navigation portlet with accordion",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        ],
      keywords='plone navigation accordion',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://bitbucket.org/redturtle/unipdgest.portlet.navigation',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['unipdgest', 'unipdgest.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.form',
          'plone.app.portlets',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
