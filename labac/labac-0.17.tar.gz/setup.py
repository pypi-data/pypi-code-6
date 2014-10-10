from distutils.core import setup
setup(
  name = 'labac',
  packages = ['labac'], # this must be the same as the name above
  version = '0.17',
  description = 'Label Based Access Control',
  author = 'Prosunjit Biswas',
  author_email = 'prosun.csedu@gmail.com',
  url = 'https://github.com/prosunjit/labac', # use the URL to the github repo
  download_url = 'https://github.com/prosunjit/labac/tarball/0.17', # I'll explain this in a second
  keywords = ['access control', 'access control list', 'acl'], # arbitrary keywords
  classifiers = [
  	  "Programming Language :: Python",
	  "Programming Language :: Python :: 2.7",
	  "Development Status :: 4 - Beta",
	  "Environment :: Other Environment",
	  "Intended Audience :: Developers",
	  "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
	  "Operating System :: OS Independent",
	  "Topic :: Software Development :: Libraries :: Python Modules",
  ],
   long_description = """\
   Label Based Access Control.
   ----------------------------
   """
)
