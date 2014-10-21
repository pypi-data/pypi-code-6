from setuptools import setup, find_packages


setup(name='futurify',
      version='0.1',
      description='Manage __future__ imports.',
      long_description=open('README.rst').read(),
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          # FIXME Coming soon!
          #'Programming Language :: Python :: 3',
          #'Programming Language :: Python :: 3.3',
      ],
      keywords='future imports syntax static analysis lint',
      url='http://github.com/storborg/futurify',
      author='Scott Torborg',
      author_email='scott@cartlogic.com',
      install_requires=[
      ],
      license='MIT',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False,
      entry_points="""\
      [console_scripts]
      futurify = futurify:main
      """)
