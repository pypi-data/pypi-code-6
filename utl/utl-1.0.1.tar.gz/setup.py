import setuptools
import sys

setuptools.setup(
    name="utl",
    version="1.0.1",

    author="xliiv",
    author_email="tymoteusz.jankowski@gmail.com",
    maintainer="xliiv",
    maintainer_email="tymoteusz.jankowski@gmail.com",

    description="""A simple tool that shows available tests without executing
    them.""",

    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'docopt',
    ],

    entry_points={
        "console_scripts": [
            "utl=utl.utl:main",
            "utl%s=utl.utl:main" % sys.version[:1],
            "utl%s=utl.utl:main" % sys.version[:3],
        ],
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Testing',
    ],
)
