import versioneer

versioneer.VCS = 'git'
versioneer.versionfile_source = 'lacore/version.py'
versioneer.versionfile_build = 'lacore/version.py'
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = 'lacore-'
from setuptools import setup, find_packages


try:
    import pandoc
    pandoc.core.PANDOC_PATH = 'pandoc'
    readme = pandoc.Document()
    readme.markdown = open('README.md').read()
    description = readme.rst
except (IOError, ImportError):
    description = 'This is the prototype client program' + \
        'for interacting with the Longaccess service.'


def pep386adapt(version):
    if version is not None and '-' in version:
        # adapt git-describe version to be in line with PEP 386
        parts = version.split('-')
        parts[-2] = 'post'+parts[-2]
        version = '.'.join(parts[:-1])
    return version


setup(version=pep386adapt(versioneer.get_version()),
      name="lacore",
      author="Konstantinos Koukopoulos",
      author_email='kk@longaccess.com',
      description="The Long Access Python SDK - Core",
      long_description=description,
      url='http://github.com/longaccess/longaccess-core/',
      license='Apache',
      packages=find_packages(exclude=['features*', '*.t']),
      install_requires=[
          'boto>=2.14, <3',
          'filechunkio>=1.5',
          'requests>=2.0.0, <3',
          'pycrypto>=2.6, <2.7',
          'PyYAML>=3.10, <4',
          'Twisted>=13.2, <14',
          'crochet>=1.0.0, <2',
          'treq>=0.2.0, <0.3',
          'python-dateutil>=2.2, <3'
          ],
      tests_require=['testtools'],
      test_suite="lacore.t",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Information Technology',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Archiving',
          'Topic :: Utilities',
          ],
      cmdclass=versioneer.get_cmdclass(),
      )
