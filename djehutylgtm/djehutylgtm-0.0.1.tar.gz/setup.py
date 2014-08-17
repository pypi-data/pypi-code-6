import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

install_requires = [
    'djehuty>=0.0.3',
    'requests>=2.3.0',
]

setup(name='djehutylgtm',
      version='0.0.1',
      description='djehutylgtm',
      long_description=README,
      author='xica development team',
      author_email='info@xica.net',
      url='https://github.com/xica/djehutylgtm',
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
              'lgtm = djehutylgtm.commands:LGTM',
          ],
      },
      )
