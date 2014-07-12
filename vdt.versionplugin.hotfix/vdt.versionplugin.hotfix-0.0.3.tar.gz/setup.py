import os
from setuptools import find_packages, setup

pkgname = "vdt.versionplugin.hotfix"

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name=pkgname,
      version="0.0.3",
      description="Create hotfix packages, these add an iteration on an existing version and do not create a tag.",
      long_description=read('README.rst'),
      author="Lars van de Kerkhof",
      author_email="lars@permanentmarkers.nl",
      url="https://github.com/devopsconsulting/vdt.versionplugin.hotfix",
      maintainer="Lars van de Kerkhof",
      maintainer_email="lars@permanentmarkers.nl",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['vdt', 'vdt.versionplugin'],
      zip_safe=True,
      install_requires=[
          "setuptools",
          "vdt.version",
          "vdt.versionplugin.default",
          "vdt.versionplugin.debianize",
      ],
      scripts = ['test-broken-apt-versioning.sh'],
      entry_points={},
)
