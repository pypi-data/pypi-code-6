#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pedro Tome <pedro.tome@idiap.ch>
# Tue 25 Mar 18:18:08 2014 CEST
#
# Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# This file contains the python (distutils/setuptools) instructions so your
# package can be installed on **any** host system. It defines some basic
# information like the package name for instance, or its homepage.
#
# It also defines which other packages this python package depends on and that
# are required for this package's operation. The python subsystem will make
# sure all dependent packages are installed or will install them for you upon
# the installation of this package.
#
# The 'buildout' system we use here will go further and wrap this package in
# such a way to create an isolated python working environment. Buildout will
# make sure that dependencies which are not yet installed do get installed, but
# **without** requiring adminstrative privileges on the host system. This
# allows you to test your package with new python dependencies w/o requiring
# administrative interventions.

from setuptools import setup, find_packages

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    # This is the basic information about your project. Modify all this
    # information before releasing code publicly.
    name='xbob.fingervein',
    version='1.0.0',
    description='Fingervein recognition based on Bob and the facereclib',
    url='http://gitlab.idiap.ch/pedro.tome/xbob.fingervein',
    license='GPLv3',
    author='Pedro Tome',
    author_email='pedro.tome@idiap.ch',
    keywords='fingervein, bob, xbob, facereclib',

    # If you have a better, long description of your package, place it on the
    # 'doc' directory and then hook it here
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,

    # This line defines which packages should be installed when you "install"
    # this package. All packages that are mentioned here, but are not installed
    # on the current system will be installed locally and only visible to the
    # scripts of this package. Don't worry - You won't need adminstrative
    # privileges when using buildout.
    install_requires=[
      'setuptools',
      'bob', # base signal proc./machine learning library
      'facereclib',
    ],

    # Your project should be called something like 'xbob.<foo>' or 
    # 'xbob.<foo>.<bar>'. To implement this correctly and still get all your
    # packages to be imported w/o problems, you need to implement namespaces
    # on the various levels of the package and declare them here. See more
    # about this here:
    # http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
    #
    # Our database packages are good examples of namespace implementations
    # using several layers. You can check them out here:
    # https://github.com/idiap/bob/wiki/Satellite-Packages
    namespace_packages = [
      'xbob',
    ],

    # This entry defines which scripts you will have inside the 'bin' directory
    # once you install the package (or run 'bin/buildout'). The order of each
    # entry under 'console_scripts' is like this:
    #   script-name-at-bin-directory = module.at.your.library:function
    #
    # The module.at.your.library is the python file within your library, using
    # the python syntax for directories (i.e., a '.' instead of '/' or '\').
    # This syntax also omits the '.py' extension of the filename. So, a file
    # installed under 'example/foo.py' that contains a function which
    # implements the 'main()' function of particular script you want to have
    # should be referred as 'example.foo:main'.
    #
    # In this simple example we will create a single program that will print
    # the version of bob.
    entry_points={

      # scripts should be declared using this entry:
      'console_scripts': [
        'fingerveinverify.py = facereclib.script.faceverify:main',
    	'scores2spoofingfile.py = xbob.fingervein.script.scores2spoofingfile:main',		
        ],
      
      # registered database short cuts
      'facereclib.database': [
        'utfvp             = xbob.fingervein.configurations.databases.utfvp:database',
        'vera              = xbob.fingervein.configurations.databases.vera:database',
      ],

      # registered preprocessings
      'facereclib.preprocessor': [
        'fingervein-preprocessor_hq = xbob.fingervein.configurations.preprocessing.finger_crop_hq:preprocessor',
        'fingervein-preprocessor_hq_heq = xbob.fingervein.configurations.preprocessing.finger_crop_hq_with_heq:preprocessor',        
        'fingervein-preprocessor_lq = xbob.fingervein.configurations.preprocessing.finger_crop_lq:preprocessor',
        'fingervein-preprocessor_lq_heq = xbob.fingervein.configurations.preprocessing.finger_crop_lq_with_heq:preprocessor',
      ],


      # registered feature extractors
      'facereclib.feature_extractor': [
        #'normalisedcrosscorr    = xbob.fingervein.configurations.features.normalised_crosscorr:feature_extractor',
        'maximumcurvature       = xbob.fingervein.configurations.features.maximum_curvature:feature_extractor',
        #'repeatedlinetracking   = xbob.fingervein.configurations.features.repeated_line_tracking:feature_extractor',
        #'widelinedetector       = xbob.fingervein.configurations.features.wide_line_detector:feature_extractor',
        #'lbp_fingervein         = xbob.fingervein.configurations.features.lbp:feature_extractor',
        
      ],

      # registered fingervein recognition algorithms
      'facereclib.tool': [
        #'miura-match-huangwl      = xbob.fingervein.configurations.tools:huangwl_tool',
        #'miura-match-huangwl-gpu  = xbob.fingervein.configurations.tools:huangwl_gpu_tool',
        'miura-match-miuramax     = xbob.fingervein.configurations.tools:miuramax_tool',
        'miura-match-miuramax-gpu = xbob.fingervein.configurations.tools:miuramax_gpu_tool',
        #'miura-match-miurarlt     = xbob.fingervein.configurations.tools:miurarlt_tool',
        #'miura-match-miurarlt-gpu = xbob.fingervein.configurations.tools:miurarlt_gpu_tool',
       ], 

      # registered SGE grid configuration files
      'facereclib.grid': [
        'gpu               = xbob.fingervein.configurations.grid.gpu:grid',
        'gpu2              = xbob.fingervein.configurations.grid.gpu2:grid',
        'gpu3              = xbob.fingervein.configurations.grid.gpu3:grid',
        'grid              = xbob.fingervein.configurations.grid.grid:grid',
        'demanding         = xbob.fingervein.configurations.grid.demanding:grid',
        'very-demanding    = xbob.fingervein.configurations.grid.very_demanding:grid',
        'gbu               = xbob.fingervein.configurations.grid.gbu:grid',
        'small             = xbob.fingervein.configurations.grid.small:grid',        
      ],

      # tests that are _exported_ (that can be executed by other packages) can
      # be signalized like this:
      'bob.test': [
        'tests = xbob.fingervein.tests.test:FingerveinTests',
        #'preprocessors       = xbob.fingervein.tests.test_preprocessing:PreprocessingTest',
        #'feature_extractors  = xbob.fingervein.tests.test_features:FeatureExtractionTest',
        #'matching            = xbob.fingervein.tests.test_matching:MatchingTest',
        
      ],
         

      # finally, if you are writing a database package, you must declare the
      # relevant entries like this:
      #'bob.db': [
      #  'example = xbob.example.driver:Interface',
      #  ]
      # Note: this is just an example, this package does not declare databases
      },

    # Classifiers are important if you plan to distribute this package through
    # PyPI. You can find the complete list of classifiers that are valid and
    # useful here (http://pypi.python.org/pypi?%3Aaction=list_classifiers).
    classifiers = [
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
)
