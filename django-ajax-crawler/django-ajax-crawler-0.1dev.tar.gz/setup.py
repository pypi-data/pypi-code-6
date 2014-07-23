import re
import sys
import os
from setuptools import setup, find_packages


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

version = get_version('ajaxcrawler')


setup(name='django-ajax-crawler',
      version=version,
      description="Handle page with dynamic data.",
      long_description=README,
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
      ],
      keywords='django crawler phantomjs',
      author='Alexander Polesov',
      author_email='alex@alex-web.ru',
      url='alex-web.ru',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'django',
          'selenium'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
