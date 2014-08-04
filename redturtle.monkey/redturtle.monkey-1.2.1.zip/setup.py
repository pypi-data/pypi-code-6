from setuptools import setup, find_packages

version = '1.2.1'
description = 'mailchimp integration for Plone.'
long_description = \
    open("README.rst").read() + "\n" + \
    open("CHANGES.rst").read()

setup(name='redturtle.monkey',
      version=version,
      description=description,
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
      ],
      keywords='',
      author='Andrew Mleczko',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/products/redturtle.monkey',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redturtle'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.app.portlets',
          'plone.app.registry',
          'postmonkey',
          'jarn.jsi18n',
      ],
      extras_require={
          'test': [
          'plone.app.testing',
          'mocker',
          'plone.mocktestcase',
          'jarn.jsi18n',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
