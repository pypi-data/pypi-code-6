from setuptools import setup

setup(name='carbonite',
      version='0.0.1',
      description='Freeze your Python package dependencies',
      author='GameChanger',
      author_email='kiril@gc.io',
      license='MIT',
      packages=['carbonite'],
      install_requires=['pip'],
      tests_require=['nose'],
      test_suite='nose.collector',
      entry_points={'console_scripts': ['carbonite = carbonite.freeze:main']},
      zip_safe=False)
