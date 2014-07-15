from setuptools import setup, find_packages
readme = open('README.txt').read()
setup(name='pySIMOD',
      version='0.2',
      author='Taylor Oshan',
      author_email='tayoshan@gmail.com',
      license='MIT',
      description='A collection of functions for spatial interaction modelling',
      long_description=readme,
      packages=find_packages())