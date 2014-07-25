from os import path
pkg_dir_path = path.dirname(path.realpath(__file__))
pkg_dir = path.basename(pkg_dir_path)

def read(fname):
    fname = path.join(path.dirname(__file__), fname)
    return open(fname).read()

from distutils.core import setup

version = "0.2"
repo_url = "https://github.com/camilin87/pkginit"

setup(
    name = pkg_dir,
    version = version,
    author = "CASH Productions",
    author_email = "support@cash-productions.com",
    description = ("Generic __index__.py generator"),
    long_description = read("README.rst"),
    license = "GPL v2",
    keywords = "package module loader init",
    url = repo_url,
    download_url = repo_url + "/tarball/" + version,
    package_data={"forecastio": ["LICENSE.txt", "README.rst"]},
    py_modules = ["pkginit"]
)
