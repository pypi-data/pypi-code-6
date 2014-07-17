from setuptools import setup, find_packages
import glob

from aticonfig_indicator import __version__

setup(name='aticonfig-indicator',
      version=__version__,
      description='Aticonfig Temp Indicator on Unity desktop.',
      long_description=open('README.rst').read(),
      url='https://github.com/syntaxsugar/aticonfig-indicator',
      license='BSD',
      platforms=['Ubuntu'],
      author='Jaromir Fojtu',
      author_email='jaromir.fojtu@gmail.com',
      scripts=["bin/aticonfig-indicator"],
      packages=['aticonfig_indicator'],
      data_files=[("share/icons/ubuntu-mono-dark/apps/24", glob.glob("icons/*")),
                  ("share/icons/ubuntu-mono-light/apps/24", glob.glob("icons/*")),
                  ("share/icons/hicolor/24x24", glob.glob("icons/*")),
      ],
      include_package_data=True,
)
