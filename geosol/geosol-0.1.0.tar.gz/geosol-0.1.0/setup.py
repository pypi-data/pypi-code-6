'''
Created on Jul 1, 2014

@author: minjoon

geosol also requires the installation of opencv (cv2)
and scikit-learn (sklearn). These must be installed
separately.
'''

from distutils.core import setup

setup(
      name='geosol',
      version='0.1.0',
      author='Min Joon Seo',
      author_email='seominjoon@gmail.com',
      packages=['geosol'],
      url='http://pypi.python.org/pypi/geosol/',
      license='LICENSE.txt',
      description='Geometry Problem Solver',
      long_description=open('README.txt').read(),
      install_requires=[
            "numpy >= 1.6.2",
            "scipy >= 0.11.0",
            "pillow >= 2.3.0",
            "scikit-learn >= 0.14.1",
            "tinyocr >= 0.2.3",
                        ],
)


