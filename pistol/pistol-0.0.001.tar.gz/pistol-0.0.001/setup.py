__author__='Dawson Reid'

import setuptools

f = open('README.md', 'r')
README = f.read()
f.close()

setuptools.setup(
  name='pistol',
  version='0.0.001',
  long_description=README,
  packages=[
    'pistol'
  ],
  package_data={
  },
  install_requires=None,
  cmdclass={
  }
)
