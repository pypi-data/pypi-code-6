from setuptools import setup, find_packages

setup(
    name = "sensate",
    version = "0.1.0",
    description = "Sensaphone hub and sensor abstraction library",
    url="https://bitbucket.org/nthmost/sensate",
    author = "InVitae Inc.",
    author_email = "developers@invitae.com",
    maintainer = "Naomi Most",
    maintainer_email = "naomi.most@invitae.com",
    license = "MIT",
    zip_safe = False,
    packages = find_packages(),
    install_requires = [ 
        'setuptools',
        'pysnmp',
    ],
)
