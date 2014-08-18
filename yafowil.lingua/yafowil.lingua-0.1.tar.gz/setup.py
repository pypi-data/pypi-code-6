import os
from setuptools import (
    setup,
    find_packages,
)


version = '0.1'
shortdesc = \
'YAFOWIL - Lingua message extrator for yafowil.yaml based forms.'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()


setup(name='yafowil.lingua',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'License :: OSI Approved :: BSD License',
      ],
      keywords='html input widgets form compound',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'http://pypi.python.org/pypi/yafowil.lingua',
      license='BSD',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['yafowil'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'PyYAML',
          'lingua>=2.5',
      ],
      test_suite="yafowil.lingua.tests.test_suite",
      entry_points="""
      [lingua.extractors]
      yafowil_yaml = yafowil.lingua.extractor:YafowilYamlExtractor
      """
      )
