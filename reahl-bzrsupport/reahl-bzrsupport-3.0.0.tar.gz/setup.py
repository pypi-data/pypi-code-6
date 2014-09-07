from setuptools import setup
setup(
    name=u'reahl-bzrsupport',
    version='3.0.0',
    description=u'Distutils support for Bazaar when using Reahl development tools.',
    long_description=u'Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nReahl-bzrsupport contains a finder for distutils for the Bazaar version control system.\n\nSee http://www.reahl.org/docs/3.0/tutorial/gettingstarted.d.html for installation instructions. ',
    url=u'http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.bzrsupport_dev'],
    py_modules=[u'setup'],
    include_package_data=False,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl'],
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    test_suite=u'reahl.bzrsupport_dev',
    entry_points={
        u'setuptools.file_finders': [
            u'reahl_finder = reahl.bzrsupport:find_files'    ],
        u'reahl.eggs': [
            u'Egg = reahl.component.eggs:ReahlEgg'    ],
                 },
    extras_require={}
)
