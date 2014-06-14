from distutils.core import setup
from setuptools import setup


setup(name='alation',
      version='0.0.1',
      packages=['alation_api'],
      entry_points={
      	'console_scripts': [
          'alation-setup = alation_api.main:setup',
          'alation-query = alation_api.main:get_sql',
          'alation-result = alation_api.main:get_result',
      	]
      }
    )
