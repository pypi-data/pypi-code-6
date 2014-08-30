import codecs
import os
import re
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = "\n" + "\n".join([read('PROJECT.txt'),])

setup(name="pyseleniumfox",
      version=find_version('pyseleniumfox', '__init__.py'),
      description="Create a firefox profile for use in selenium tests that includes a preconfigured selenium IDE, so that you can debug and write tests on the fly.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Build Tools',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
#          'Programming Language :: Python :: 3',
#          'Programming Language :: Python :: 3.1',
#          'Programming Language :: Python :: 3.2',
#          'Programming Language :: Python :: 3.3',
      ],
      keywords='firefox selenium ide tool',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      license='MIT',
      install_requires=['selenium>=2.42'],
      packages=find_packages(exclude=["contrib", "docs", "tests*"]),
      package_data={'': ['selenium-ide.xpi', 'pythonformatters@seleniumhq.org.xpi']},
      zip_safe=False,
)
