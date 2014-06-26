from setuptools import setup, find_packages
import graphiti

packages = find_packages(".")

setup(
    name="graphiti",
    version=graphiti.__version__,
    author="ASD Technologies",
    author_email="admin@asdco.ru",
    description="Graphite/Carbon client",
    license="Private",
    url="https://bitbucket.org/asdtech/graphiti",
    packages=packages,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "License :: Other/Proprietary License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2.6",
    ],
)
