import xstatic.pkg.jreject as xst

# The README.txt file should be written in reST so that PyPI can use
# it to generate your project's PyPI page. 
long_description = open('README.txt').read()

from setuptools import setup, find_packages

setup(
    name=xst.PACKAGE_NAME,
    version=xst.PACKAGE_VERSION,
    description=xst.DESCRIPTION,
    long_description=long_description,
    classifiers=xst.CLASSIFIERS,
    keywords=xst.KEYWORDS,
    maintainer=xst.MAINTAINER,
    maintainer_email=xst.MAINTAINER_EMAIL,
    license=xst.LICENSE,
    url=xst.HOMEPAGE,
    platforms=xst.PLATFORMS,
    packages=find_packages(),
    namespace_packages=['xstatic', 'xstatic.pkg', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],  # nothing! :)
                          # if you like, you MAY use the 'XStatic' package.
)
