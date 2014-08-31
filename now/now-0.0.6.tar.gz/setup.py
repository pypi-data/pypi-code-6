from setuptools import setup

with open("README.rst", "r") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="now",
    version="0.0.6",
    packages=["now"],
    scripts=["scripts/now"],
    entry_points = {
        'console_scripts': ['now = now.main:main'],
     },
    description="Record what you are doing SIMPLY from the command line",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    url="https://github.com/sashahart/now",
    author="Sasha Hart",
    author_email="s@sashahart.net",
)
