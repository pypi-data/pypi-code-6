import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(name='restzzz',
      version=0.1,
      description='REST-ful API for 0mq',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords="web services",
      author='Matt Soucy',
      author_email='msoucy@csh.rit.edu',
      url='http://code.msoucy.me/RESTZZZ',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['cornice', 'waitress', "PyYAML", "pyzmq"],
      entry_points = """\
      [paste.app_factory]
      main = restzzz:main
      """,
      paster_plugins=['pyramid'])
