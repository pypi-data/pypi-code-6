from setuptools import setup, find_packages
import os

version = '1.3rc2'

setup(name='ityou.ESI',
      version=version,
      description="ITYOU ESI - A Social Intranet Solution based on Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Social Intranet, Plone, Activity Stream, Instant Messaging, Who is Online',
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
        'ityou.workflow',
        #'ityou.qrcode',
        'sqlalchemy',
        'redis',
        'hiredis',
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
