from setuptools import setup, find_packages

setup(
    name = "ecosynth",
    version = "0.1",
    packages = find_packages(),
    scripts = [],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['numpy', 'scipy', 'matplotlib', 'utm', 'bottle'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*md', '*.css', '*.js', '*.html' ],
    },

    # metadata for upload to PyPI
    author = "Will B",
    author_email = "willb2@umbc.edu",
    description = "Ecosynth Processing Library",
    license = "Creative Commons Attribution 4.0 International",
    keywords = "point-clouds CV ecology",
    url = "http://www.ecosynth.org",

    # could also include long_description, download_url, classifiers, etc.
)
