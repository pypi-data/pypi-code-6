from setuptools import find_packages, setup

setup(
    # Metadata
    name="mdma",
    version="0.1.2",
    description="ipython notebook markdown magic",
    url="",
    author="Erik Gafni",
    author_email="egafni@gmail.com",
    maintainer="Erik Gafni",
    maintainer_email="egafni@gmail.com",
    license="GPLv2",
    install_requires=["markdown", ],
    # Packaging Instructions
    packages=find_packages(),
    include_package_data=True
)