from setuptools import setup

long_description = \
'''

BarkingOwl is a scalable web crawler intended to be used to
find specific document types on websites, such as PDFs, XLS, 
TXT, HTML, etc.

'''

setup(
    name="BarkingOwl",
    version="0.0.18",
    license="GPL3",
    author="Timothy Duffy",
    author_email="tim@timduffy.me",
    packages=["barking_owl", "barking_owl.scraper", "barking_owl.dispatcher"],
    zip_safe=False,
    description='Scalable web crawler.',
    long_description=long_description,
    include_package_data=True,
    platforms="any",
    install_requires=[
      "beautifulsoup4==4.3.2",
      "libmagic==1.0",
      "pika==0.9.13",
      "python-dateutil==2.2",
      "python-magic==0.4.6",
      "six==1.5.2",
      "wsgiref==0.1.2",
    ], 
    url="https://github.com/thequbit/BarkingOwl",
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      #'Operating System :: POSIX',
    ],
)
