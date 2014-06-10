from setuptools import setup, find_packages
from distutils.extension import Extension
import numpy

ext_modules = [
    Extension("ivi.optimizations",
              ["ivi/optimizations.c"],
              include_dirs=[numpy.get_include()]
              )
]

version = (1, 0, 0)

description = "fast and responsive viewer for peptide identifications from IMSB workflows."

setup(name="ivi",
      description=description,
      maintainer="Uwe Schmitt",
      maintainer_email="uwe.schmitt@id.ethz.ch",
      license="http://opensource.org/licenses/BSD-3-Clause",
      platforms=["any"],

      packages=find_packages(exclude=["tests"]),
      version="%d.%d.%d" % version,
      entry_points={
          "gui_scripts": ["ivi = ivi.cmdline:main",
                          "ivi.prepare = ivi.cmdline:prepare", ]

      },
      include_package_data=True,
      zip_safe=False,
      install_requires=["tables"],
      ext_modules=ext_modules,
      )
