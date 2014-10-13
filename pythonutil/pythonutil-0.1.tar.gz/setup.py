from distutils.core import setup
setup(
  name = 'pythonutil',
  packages = ['pythonutil'], # this must be the same as the name above
  version = '0.1',
  description = 'Python Utilities of Miscellanious Scripts',
  author = 'Prosunjit Biswas',
  author_email = 'prosun.csedu@gmail.com',
  url = 'https://github.com/Prosunjit/pythonutil', # use the URL to the github repo
  download_url = 'https://github.com/prosunjit/pythonutil/tarball/0.1', # I'll explain this in a second
  keywords = ['python Utility'], # arbitrary keywords
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
   Python Utilities of Miscellanious Scripts.
   ------------------------------------------
   Includes:
       OpenStack keystone Util: generate token, get tenant_id so on.
       JSONUtil: Load JSON from a file, or a String with UTF-8 encoding
       FileUtil: Simply reads a file
   """
)
