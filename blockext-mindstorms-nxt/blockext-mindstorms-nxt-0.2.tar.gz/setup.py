import re
from setuptools import setup


version = re.search("__version__ = '([^']+)'",
                    open('blockext_mindstorms_nxt/__init__.py').read()).group(1)


setup(name = 'blockext-mindstorms-nxt',
      version = version,
      author = 'Tim Radvan, Connor Hudson',
      author_email = 'blob8108@gmail.com',
      url = 'https://github.com/blockext/mindstorms-nxt',
      description = 'Lego Mindstorms NXT extension for Scratch 2.0 and Snap!',
      license = 'MIT',
      packages = ['blockext_mindstorms_nxt'],
      install_requires = [
          'blockext == 0.2.0a2',
          'nxt-python',
      ],
      classifiers = [
        "Programming Language :: Python",
      ],
)
