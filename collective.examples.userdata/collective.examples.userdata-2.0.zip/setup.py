from setuptools import setup, find_packages
import os

version = '2.0'
long_description = open("README.rst").read() + "\n"\
    + open(os.path.join("docs", "HISTORY.txt")).read() + "\n"\
    + open(os.path.join("docs", "TODO.txt")).read(),

setup(
    name='collective.examples.userdata',
    version=version,
    description="Showcase for the new (Plone 4) plone.app.users "
                "IUserDataSchema. Shows how to extend the user data fields "
                "that can be selected for the registration form.",
    long_description=long_description,
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Kees Hink',
    author_email='',
    url='https://github.com/collective/collective.examples.userdata',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.examples'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.users >= 2.0',
        'plone.formwidget.datetime [z3cform]',
    ],
    extras_require={
        'test': ['plone.app.testing'],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
