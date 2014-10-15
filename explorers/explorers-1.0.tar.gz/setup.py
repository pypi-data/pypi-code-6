import os
from setuptools import setup

setup(
    name         = "explorers",
    version      = "1.0",
    author       = "Fabien Benureau",
    author_email = "fabien.benureau@inria.fr",
    description  = 'Framework for autonomous exploration algorithms in sensorimotor spaces',
    license      = "Open Science (see fabien.benureau.com/openscience.html",
    keywords     = "exploration learning algorithm sensorimotor robots robotics",
    url          = "flowers.inria.fr",
    packages=[
        'explorers',
        'explorers.algorithms',
        'explorers.algorithms.reuse',
        'explorers.algorithms.im',
    ],
    dependency_links=[
        "https://github.com/flowersteam/forest/tarball/master#egg=forest-1.0",
    ],
    install_requires=['forest', 'learners'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
    ]
)
