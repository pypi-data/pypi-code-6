from setuptools import setup


setup(name='alation-api',
      version='2.0',
      packages=['alation'],
      entry_points={
      'console_scripts': [
          'alation-setup = alation.main:setup',
          'alation-query = alation.main:print_sql',
          'alation-result = alation.main:print_result',
      ]
      }
      )
