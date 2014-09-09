from setuptools import setup, find_packages
import glob

setup(
    name = "pyrannosaurus",
    version = "0.0.6",
    description = "Salesforce Development Tools",
    author = "KC Shafer",
    author_email = "kclshafer@gmail.com",
    url = "https://github.com/kcshafer/pyrannosaurus/",
    keywords = ["salesforce"],
    install_requires = [
        "suds==0.4",
        "lxml",
        ],
    package_dir={},
    include_package_data=True,
    packages=find_packages() + ['wsdl'],
    package_data={
       'wsdl' : ['wsdl/*.xml']
    },
    long_description = """\
    Salesforce Development Tools
    ----------------------------
    """
)
