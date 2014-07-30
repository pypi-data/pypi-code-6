from setuptools import setup

setup(name='nlmpy',
      version='0.1',
      description='A Python package to create neutral landscape models',
      author="Thomas R. Etherington, E. Penelope Holland, and David O'Sullivan",
      author_email='thomas.etherington@aut.ac.nz',
      license='Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License (http://creativecommons.org/licenses/by-nc-sa/3.0/)',
      packages=['nlmpy'],
      install_requires=[
          'numpy',
          'scipy',
      ],
      zip_safe=False)