import multiprocessing
from setuptools import setup, find_packages
import os
import glob


#*********
#pathToData = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pymysql_utils/data')
#print('*******************' + pathToData)
#print(pathToData)
#datadir = os.path.join('pymysql_utils', 'data')
#datafiles = [(datadir, [f for f in glob.glob(os.path.join(datadir, '*'))])]
#print('***************' + str(datafiles))
#*********

setup(
    name = "pymysql_utils",
    version = "0.44",
    packages = find_packages(),

    # Dependencies on other packages:
    # Couldn't get numpy install to work without
    # an out-of-band: sudo apt-get install python-dev
    setup_requires   = [],
    install_requires = [#'pymysql3>=0.5',
                        'MySQL-python>=1.2.5',
			'configparser>=3.3.0'
			],
    tests_require    = ['sentinels>=0.0.6', 'nose>=1.0'],

    # Unit tests; they are initiated via 'python setup.py test'
    test_suite       = 'nose.collector', 

#    package_dir = {'pymysql_utils': 'pymysql_utils'},
#    package_data = {
      # DOES NOT WORK: 'pymysql_utils': ['data/*.csv']
      #'pymysql_utils': [os.path.join(pathToData,'/*.csv')]
      #'pymysql_utils.data': [os.path.join(pathToData,'/*.csv')]
      # If any package contains *.txt or *.rst files, include them:
      #   '': ['*.txt', '*.rst'],
      # And include any *.msg files found in the 'hello' package, too:
      #   'hello': ['*.msg'],
      #'': ['ipToCountrySoftware77DotNet.csv'],
#      'pymysql_utils': ['ipToCountrySoftware77DotNet.csv'],
#    },
    #data_files = datafiles,
    #[
      #(pathToData, ['ipToCountrySoftware77DotNet.csv'])
      #('/home/paepcke/EclipseWorkspaces/pymysql_utils/pymysql_utils/data', ['ipToCountrySoftware77DotNet.csv'])
      #('/home/paepcke/EclipseWorkspaces/pymysql_utils/pymysql_utils/data', ['./*'])
      
    #  ],

    # metadata for upload to PyPI
    author = "Andreas Paepcke",
    author_email = "paepcke@cs.stanford.edu",
    description = "Thin wrapper around pymysql. Provides Python iterator for queries. Abstracts away cursor.",
    license = "BSD",
    keywords = "MySQL",
    url = "https://github.com/paepcke/pymysql_utils",   # project home page, if any
)
