import sys
assert sys.version >= '2' , 'Install Python 2.0 or greater'

from setuptools import setup, find_packages

# $Id: setup.py,v 1.2 2007/05/10 16:17:05 jay Exp $

def runSetup ():
    setup(name='pinv',
          version='0.0.1a',
          author='Branko Toic' ,
          author_email='branko@toic.org' ,
          url='https://bitbucket.org/btoic/python-pinv/get/master.tar.gz' ,
          license='GPLv2' ,
          platforms=[ 'unix' ] ,
          description='pinv is pluggable inventory service' ,
          packages=find_packages(),
          scripts=['pinv-run.py'],
          provides=['pinv'],
    )

if __name__ == '__main__':
    runSetup()
