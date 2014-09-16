#!/usr/bin/env python
import setuptools

from PyOLP import __version__

if __name__ == "__main__":
    setuptools.setup(
        name="PyOLP",
        version=__version__,
        description="Python library implementing the Oregon Liquor Prices V1 API",
        license="GPL3",
        author="Cameron Brandon White",
        author_email="cameronbwhite90@gmail.com",
        url="https://github.com/cameronbwhite/PyOLP",
        download_url="https://github.com/cameronbwhite/PyOLP/downloads",
        provides=[
            "PyOLP",
        ],
        packages=[
            "PyOLP",
            "PyOLP.tests"
        ],
        package_data={
            'PyOLP': ["COPYING", "COPYING.LESSER", "README.md"],
        },
        classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.7",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        test_suite="PyOLP.tests.AllTests",
        include_package_data=True,
        use_2to3=True,
    )
