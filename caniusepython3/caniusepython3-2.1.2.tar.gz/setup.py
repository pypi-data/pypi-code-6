from setuptools import setup

import os


# Installed name used for various commands (both script and setuptools).
command_name = os.environ.get('CIU_ALT_NAME') or 'caniusepython3'

with open('README_PyPI.rst') as file:
    long_description = file.read()

setup(name='caniusepython3',
      version='2.1.2',
      description='Determine what projects are blocking you from porting to Python 3',
      long_description=long_description,
      author='Brett Cannon',
      author_email='brett@python.org',
      url='https://github.com/brettcannon/caniusepython3',
      packages=['caniusepython3', 'caniusepython3.test'],
      include_package_data=True,
      install_requires=['distlib', 'setuptools', 'pip',  # Input flexibility
                        'argparse', 'futures',  # Functionality
                        'mock'],  # Testing
      test_suite='caniusepython3.test',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      entry_points={
          'console_scripts': [
              '{0} = caniusepython3.__main__:main'.format(command_name),
          ],
          'distutils.commands': [
              '{0} = caniusepython3.command:Command'.format(command_name),
          ],
      },
      zip_safe=True,
)
