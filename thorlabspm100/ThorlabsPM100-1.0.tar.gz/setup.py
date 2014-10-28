# -*- coding: latin-1 -*-
import sys

#from distutils.core import setup
from setuptools import setup

from ThorlabsPM100 import __long_description__, __version__

doc_url = "http://pythonhosted.org/RigolDG5000"

setup(name="ThorlabsPM100", version=__version__,
      author=u'Pierre Cladé', author_email="pierre.clade@spectro.jussieu.fr",
      maintainer=u'Pierre Cladé',
      maintainer_email="pierre.clade@spectro.jussieu.fr",
      license='''\
This software can be used under one of the following two licenses: \
(1) The BSD license. \
(2) Any other license, as long as it is obtained from the original \
author.''',

      description='Interface to the PM100A/D power meter from Thorlabs.',
      long_description = __long_description__,  
      keywords=['Thorlabs','PM100', 'PM100A', 'PM100D'],
      url = doc_url,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'], 
#     requires=['pyvisa'],
     packages=["ThorlabsPM100", ]
)
