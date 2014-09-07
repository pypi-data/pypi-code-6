from setuptools import setup
setup(
    name=u'reahl-mailutil',
    version='3.0.0',
    description=u'Simple utilities for sending email from Reahl.',
    long_description=u'Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nReahl-mailutil is a simple library for sending emails (optionally from ReST sources).\n\nSee http://www.reahl.org/docs/3.0/tutorial/gettingstarted.d.html for installation instructions. ',
    url=u'http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.mailutil_dev', 'reahl.mailutil'],
    py_modules=[u'setup'],
    include_package_data=False,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl'],
    install_requires=['reahl-component>=3.0,<3.1', 'docutils>=0.12,<0.12'],
    setup_requires=[],
    tests_require=['reahl-tofu>=3.0,<3.1', 'reahl-stubble>=3.0,<3.1'],
    test_suite=u'reahl.mailutil_dev',
    entry_points={
        u'reahl.configspec': [
            u'config = reahl.mailutil.reusableconfig:MailConfig'    ],
        u'reahl.eggs': [
            u'Egg = reahl.component.eggs:ReahlEgg'    ],
                 },
    extras_require={}
)
