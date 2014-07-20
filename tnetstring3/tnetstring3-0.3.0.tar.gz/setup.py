from setuptools import setup, Extension

def get_info():
    info = {}
    src = open("tnetstring/__init__.py")
    lines = []
    ln = next(src)
    while "__version__" not in ln:
        lines.append(ln)
        ln = next(src)
    while "__version__" in ln:
        lines.append(ln)
        ln = next(src)
    exec("".join(lines),info)
    return info

info = get_info()

setup(name="tnetstring3",
      version=info["__version__"],
      author="Carlo Pires",
      author_email="carlopires@gmail",
      url="http://github.com/carlopires/tnetstring",
      description="data serialization using typed netstrings",
      long_description=info["__doc__"],
      license="MIT",
      keywords="netstring serialization",
      packages=["tnetstring"],
      ext_modules = [
          Extension(name="_tnetstring", sources=["tnetstring/_tnetstring.c"]),
      ],
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License"
        ],
      test_suite='tests.suite'
     )

