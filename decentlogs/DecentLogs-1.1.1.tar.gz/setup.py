import os
from setuptools import setup, find_packages

version = "1.1.1"

description = """ Simple library to have objects keeping their log messages. """ 

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
long_description = read('README.md')
    

setup(name='DecentLogs',
      author="Andrea Censi",
      author_email="censi@mit.edu",
      url='http://github.com/AndreaCensi/decent_logs',
      
      description=description,
      long_description=long_description,
      keywords="",
      license="",
      
      classifiers=[
        'Development Status :: 4 - Beta',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        # 'Topic :: Software Development :: Quality Assurance',
        # 'Topic :: Software Development :: Documentation',
        # 'Topic :: Software Development :: Testing'
      ],

      version=version,
      download_url='http://github.com/AndreaCensi/decent_logs/tarball/%s' % version,
      
      entry_points={
        'console_scripts': [
       # 'comptests = comptests:main_comptests'
       ]
      },
      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=['PyContracts'],
      tests_require=['nose'],
)

