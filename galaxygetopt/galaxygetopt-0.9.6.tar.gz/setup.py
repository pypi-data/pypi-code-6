from setuptools import setup
# Read in long description
long_description=open('README-PYPI.rst').read()

setup(name='galaxygetopt',
      version='0.9.6',
      description='Argparse Wrapper for Galaxy',
      author='Eric Rasche',
      author_email='rasche.eric@yandex.ru',
      url='https://cpt.tamu.edu/gitlab/cpt/pygetoptwrapper/',
      packages=['galaxygetopt', 'galaxygetopt.parameter', 'galaxygetopt.writer'],
      license='GPL3',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Environment :: Console'
      ],
      long_description=long_description,
      install_requires=['jinja2'],
)
