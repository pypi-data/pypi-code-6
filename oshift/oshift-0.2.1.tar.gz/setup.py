from setuptools import setup, find_packages
setup(
    name = "oshift",
    version = "0.2.1",
    packages = find_packages(),
    install_requires = ['requests'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['README', '*.rst', '*.txt'],
    },

    # metadata for upload to PyPI
    author = "Ryan Brown",
    author_email = "ryansb@redhat.com",
    description = "This is a fork of the python interface for the new Openshift REST API.",
    license = "Unknown",
    keywords = "PaaS Redhat OpenShift",
    url = "https://github.com/ryansb/python-interface",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
    entry_points = """
    [console_scripts]
    oshift = oshift:command_line
    """,
)
