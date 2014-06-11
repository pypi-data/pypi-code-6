from setuptools import setup, find_packages
import os

version = '1.4.3'

setup(name='quintagroup.formlib.captcha',
      version=version,
      description="Captcha field for formlib based on "
                  "quintagroup.captcha.core package",
      long_description=open("README.txt").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 3.2",
          "Framework :: Plone :: 3.3",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Framework :: Zope2",
          "Framework :: Zope3",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Security",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone formlib captcha',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://svn.quintagroup.com/products/quintagroup.formlib.captcha',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup', 'quintagroup.formlib'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'quintagroup.captcha.core >= 0.4.3',
          'zope.app.form',
          'zope.formlib',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
