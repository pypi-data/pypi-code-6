from setuptools import setup
setup(
      name         = 'SVGCompress',
      packages     = ['SVGCompress'],
      version      = '0.12',
      description  = 'Compress svg graphics',
      author       = 'Gen Del Raye',
      author_email = 'gdelraye@hawaii.edu',
      url          = '',
      download_url = '',
      keywords     = ['figure', 'vector', 'svg', 'compression'],
      requires     = ['numpy', 'shapely', 'xml', 'svg.path', 'copy', 'rdp'],
      package_data = {'': ['*.svg']},
      classifiers  = [
              "Intended Audience :: Science/Research",
              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
              "Natural Language :: English",
              "Operating System :: OS Independent",
              "Programming Language :: Python",
              "Topic :: Scientific/Engineering",
              "Topic :: Scientific/Engineering :: Visualization"],
      )