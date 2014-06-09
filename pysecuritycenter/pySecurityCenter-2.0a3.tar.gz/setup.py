from setuptools import setup
import securitycenter

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name="pySecurityCenter",
    version=securitycenter.__version__,
    description="Security Center API Library",
    long_description=read_md('README.md'),
    author=", ".join(securitycenter.__authors__),
    author_email="steve@chigeek.com",
    url="https://github.com/SteveMcGrath/pySecurityCenter",
    packages=[
        "securitycenter",
        "securitycenter.orm",
        "securitycenter.orm.modules",
    ],
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ]
)
