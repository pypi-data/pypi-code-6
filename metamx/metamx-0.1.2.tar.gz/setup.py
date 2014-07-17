from setuptools import setup, find_packages

setup(
  name='metamx',
  version='0.1.2',
  author='ops',
  author_email='ops@metamarkets.com',
  packages=['metamx'],
  package_data={'':'config.yaml'},
  url='https://github.com/metamx/operations',
  description='Metamx Operations API',
  install_requires=['boto','pyyaml'],
)
