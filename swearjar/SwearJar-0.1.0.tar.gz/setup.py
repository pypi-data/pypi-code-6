from distutils.core import setup

setup(
    # Application name:
    name="SwearJar",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Anthony D'Andrea, Rod Dennis, Mike Spann, Sean Dennison",
    author_email="anthony.dandrea@me.com, rdnydnns@gmail.com, michaeljspann@gmail.com, sean.dennison.osu@gmail.com",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/SwearJar_v010/",

    #
    # license="LICENSE.txt",
    description="Reddit bot + web application that exposes the swears of the Reddit nation",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "Flask",
        "praw",
        "flask-wtf",
        "flask-assets"
    ],
)
