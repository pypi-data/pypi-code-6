# python imports
import os
from setuptools import find_packages
from setuptools import setup

# lfs imports
from lfs import __version__

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

setup(name='django-lfs',
      version=__version__,
      description='LFS - Lightning Fast Shop',
      long_description=README,
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      keywords='django e-commerce online-shop',
      author='Kai Diefenbach',
      author_email='kai.diefenbach@iqpp.de',
      url='http://www.getlfs.com',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      dependency_links=["http://pypi.iqpp.de/"],
      install_requires=[
          'setuptools',
          'django-compressor == 1.4',
          'django-localflavor == 1.0',
          'django-paypal == 0.1.2.lfs-1',
          'django-pagination == 1.0.7',
          'django-portlets == 1.1.1',
          'django-postal == 0.95',
          'django-reviews == 1.0',
          'django-tagging == 0.3.1',
          'lfs-contact == 1.1',
          'lfs-order-numbers == 1.0b1',
          'lfs-paypal == 1.2',
          'lfs-theme == 0.8.0a1',
          'Pillow == 2.4.0',
          'South == 0.8.4',
      ],
      )
