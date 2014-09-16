from setuptools import setup, find_packages
import os

version = '1.3rc3'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='ityou.esi.theme',
      version=version,
      description="ITYOU ESI Theme",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='ITYOU/LM',
      author_email='lm@ityou.de',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['ityou', 'ityou.esi'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
            'ityou.esi.viewlets',
            'ityou.jsonapi',
            'ityou.whoisonline',
            'ityou.extuserprofile',
            'ityou.astream',
            'ityou.imessage',
            'ityou.dragdrop',
            'ityou.thumbnails',
            'ityou.follow',
            'ityou.notify',
            #'ityou.qrcode',
            'webcouturier.dropdownmenu', 
            'Solgema.fullcalendar',
            'collective.quickupload',
            'sqlalchemy',
            'redis',
            'hiredis',
            'psycopg2',
          ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
