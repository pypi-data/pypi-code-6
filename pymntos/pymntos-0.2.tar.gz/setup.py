from setuptools import setup

setup(name='pymntos',
      version='0.2',
      description='PyMNtos library',
      url='http://bitbucket.org/wyattwalter/pymntos-lib',
      author='Wyatt Walter',
      author_email='wyattwalter@gmail.com',
      license='MIT',
      packages=['pymntos'],
      install_requires=[
          'docopt',
      ],
      scripts=['bin/pymntos'])
