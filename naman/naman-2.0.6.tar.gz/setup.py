import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name = 'naman',
    version = '2.0.6',
    packages = find_packages(),
    include_package_data = True,
    license = 'BSD License',
    description = 'A Django project IPAM tool',
    long_description = README,
#TODO set the project's home page
    url = 'http://blog.digitalhigh.es',
    author = 'Javier Pardo Blasco(jpardobl)',
    author_email = 'jpardo@digitalhigh.es',
    install_requires = (
      "Django==1.5",
      "MySQL-python",
      "argparse",
      "django-extensions",
      "djangorestframework",
      "ipaddr",
      "requests",
      "pyparsing",
      "simplejson",
      "gunicorn",
    ),
    
  #  test_suite='test_project.tests.runtests',
   # tests_require=("selenium", "requests"),
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)