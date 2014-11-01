from setuptools import setup, find_packages

setup(
    name='hgdiffmetrics',
    version='1.0.dev1',
    description='Mercurial extension for using diffmetrics',
    author='Neal Finne',
    author_email='neal@nealfinne.com',
    url='https://bitbucket.org/nfinne/hgdiffmetrics',
    packages=find_packages(),
    install_requires=['diffmetrics'],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
