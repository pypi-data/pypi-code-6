from setuptools import setup, find_packages
import os

version = '0.1.5'

setup(name='plonetheme.INTKmodern',
    version=version,
    description="An installable Diazo theme for Plone 4",
    long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Andre Goncalves',
    author_email='andre@intk.com',
    url='https://github.com/intk/plonetheme.INTKmodern',
    download_url='https://github.com/intk/plonetheme.INTKmodern/tarball/0.1.5',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plonetheme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
	'plone.app.theming',
    ],
    extras_require={
        "test": ["plone.app.testing"]
    },
    entry_points={
        "z3c.autoinclude.plugin": "target = plone",
    }
)
