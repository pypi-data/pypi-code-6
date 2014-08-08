from distutils.core import setup

setup(
  author="Jeremy Shute",
  author_email="j@altschool.com",
  description="AltSchool JSON-RPC compatibility library",
  install_requires=open("requirements.txt").readlines(),
  long_description=open("README.rst").read(),
  name="pyjsonrpc",
  packages=["pyjsonrpc"],
  url="http://github.com/AltSchool/pyjsonrpc",
  # The following version is automatically computed by the Makefile.
  version="0.0.1",
)
