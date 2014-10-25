import setuptools


setuptools.setup(
    name="devbliss-jazz", version="0.1.0",
    packages=setuptools.find_packages(),
    test_suite="jazz.tests",
    author="Stefano Palazzo",
    author_email="stefano.palazzo@gmail.com",
    url="https://github.com/sfstpala/jazz/",
    license="ISC License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    install_requires=[
        "docopt >=0.6.2",
        "tornado >=4.0.2",
    ],
    entry_points={
        "console_scripts": [
            "jazz = jazz.__main__:main",
        ]
    },
    package_data={
        "jazz": [
            "templates/*.html",
            "static/*.css",
        ],
    },
)
