from distutils.core import setup
import pychart.version

setup (name = "Python-Chart",
       version = pychart.version.version,
       description = "Python Chart Generator",
       author = "Yasushi Saito",
       author_email = "barsintod@gmail.com",
       url = "http://www.hpl.hp.com/personal/Yasushi_Saito/pychart",
       license = "GPL",
       long_description = """
NOTE: I changed the email just to be able to upload it at pypi
but this project is copyright by Yasushi Saito <yasushi@cs.washington.edu>
Pychart is a Python library for creating high-quality
charts in Postscript, PDF, PNG, and SVG. 
It produces line plots, bar plots, range-fill plots, and pie
charts.""",
       packages = ['pychart', 'pychart.afm']
      )
