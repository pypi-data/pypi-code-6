import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

install_requires = [
    'djehuty>=0.0.3',
    'suddendeath==0.3.1',
    'twitter',
]

setup(name='djehutysuddendeath',
      version='0.1.0',
      description='suddendeath generator for djehuty',
      long_description=README,
      author='xica development team',
      author_email='info@xica.net',
      url='https://github.com/xica/djehuty-suddendeath',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Pyramid',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Communications :: Chat',
      ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=install_requires,
      test_suite='djehutylgtm',
      entry_points={
          'djehuty.commands': [
              'suddendeath = djehutysuddendeath.commands:Suddendeath',
          ],
      },
      )
