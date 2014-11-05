import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.org')).read()

setup(name='tagrelease',
      version='1.0.2',
      long_description=README,
      classifiers=[
	  "Programming Language :: Python",
      ],
      install_requires = ['GitPython', 'pyyaml', 'argdeclare'],
      author='Parnell Springmeyer',
      author_email='parnell@plumlife.com',
      keywords='git release tagging script plum',
      scripts=['tagrelease'],
      url="https://github.com/plumlife/tagrelease",
      zip_safe=False
      )
