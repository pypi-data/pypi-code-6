from setuptools import setup

setup(
  name='metamx',
  version='0.1.1',
  author='ops',
  author_email='ops@metamarkets.com',
  packages=['metamx'],
  url='https://github.com/metamx/operations',
  description='Metamx Operations API',
  install_requires=['boto','pyyaml'],
)
