from setuptools import setup

setup(name='carbonite',
      version='0.0.9',
      description='Freeze your Python package dependencies',
      url='https://github.com/gamechanger/carbonite',
      author='GameChanger',
      author_email='kiril@gc.io',
      license='MIT',
      packages=['carbonite'],
      install_requires=['pip'],
      tests_require=['nose'],
      test_suite='nose.collector',
      entry_points={'console_scripts': ['carbonite = carbonite.freeze:main']},
      zip_safe=False)
