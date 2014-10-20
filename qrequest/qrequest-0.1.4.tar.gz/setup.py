from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

def license():
    with open('LICENSE') as f:
        return f.read()

setup(name='qrequest',
      version='0.1.4',
      description='Instantly create an API and web interface for SQL queries.',
      long_description=readme(),
      url='https://github.com/benjamin-croker/qrequest',
      author='Benjamin Croker',
      author_email='benjamin.croker@gmail.com',
      license=license(),
      packages=['qrequest'],
      install_requires=['flask'],
      entry_points = {
        'console_scripts': ['qrequest=qrequest.main:main'],
      },
      zip_safe=False)