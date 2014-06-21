import re
from setuptools import setup

with open('autosort/__init__.py') as f:
    version = re.search(r'''^__version__\s+=\s+['"](.+)['"]''',
                        f.read(), re.M).group(1)


setup(name='autosort',
      author='Fredrik Bergroth',
      author_email='fbergroth@gmail.com',
      version=version,
      url='https://github.com/fbergroth/autosort',
      license='MIT',
      packages=['autosort'],
      description='Automatically sort import statements.')
