
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='servicemanager',
      version='0.0.2',
      description='A python tool to manage developing and testing with lots of microservices',
      url='https://github.com/hmrc/service-manager',
      author='vaughansharman',
      license='Apache Licence 2.0',
      packages=['servicemanager', 'servicemanager.actions', 'servicemanager.server', 'servicemanager.service', 'servicemanager.thirdparty'],
      install_requires=required,
      scripts=['bin/sm.py'],
      zip_safe=False)
