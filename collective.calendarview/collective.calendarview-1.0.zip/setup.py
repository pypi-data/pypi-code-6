import os
from setuptools import setup, find_packages

version = '1.0'

setup(name='collective.calendarview',
      version=version,
      description="Fullcalendar view",
      long_description=(
          open("README.txt").read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read()
      ),
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.configviews',
          'collective.js.fullcalendar'
      ],
      extras_require={
          'test': [
              'plone.app.testing'
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
