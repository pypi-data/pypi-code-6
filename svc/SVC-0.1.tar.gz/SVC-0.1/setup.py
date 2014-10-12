from setuptools import setup

setup(name="SVC",
      version="0.1",
      description="Spreadsheet Viewer and Converter",
      author="Aritz Tusell",
      author_email="aritztg at gmail",
      url="https://github.com/aritztg/svc",
      license="GPL",
      scripts=["svc"],
      install_requires = ["xlrd>=0.9.3"]
)