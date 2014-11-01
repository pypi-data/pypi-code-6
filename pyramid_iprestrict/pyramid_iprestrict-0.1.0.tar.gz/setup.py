from setuptools import setup, find_packages
import sys, os

setup(
    name='pyramid_iprestrict',
    version="0.1.0",
    description="IP based restriction tween for pyramid",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
    ],
    keywords="web wsgi pyramid ipaddress",
    author="xica development team",
    author_email="info@xica.net",
    url="https://github.com/xica/pyramid_iprestrict",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ipaddress",
        "pyramid",
    ],
    extras_require = {
        "testing": [
            "nose",
            "coverage",
        ]
    },
    test_suite="pyramid_iprestrict",
)
