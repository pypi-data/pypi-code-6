from setuptools import setup
setup(
    name=u'reahl-webdev',
    version='3.0.0',
    description=u'Web-specific development tools for Reahl.',
    long_description=u'Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nReahl development tools for testing and working with web based programs.\n\nSee http://www.reahl.org/docs/3.0/tutorial/gettingstarted.d.html for installation instructions. ',
    url=u'http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.webdev'],
    py_modules=[u'setup'],
    include_package_data=True,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl'],
    install_requires=['reahl-web>=3.0,<3.1', 'reahl-dev>=3.0,<3.1', 'reahl-component>=3.0,<3.1', 'reahl-tofu>=3.0,<3.1', 'lxml>=3.3,<3.3.999', 'WebTest>=2.0,<2.0.999', 'selenium>=2.42,<2.42.999'],
    setup_requires=[],
    tests_require=['reahl-tofu>=3.0,<3.1', 'reahl-stubble>=3.0,<3.1'],
    test_suite=u'tests',
    entry_points={
        u'reahl.eggs': [
            u'Egg = reahl.component.eggs:ReahlEgg'    ],
        u'reahl.dev.commands': [
            u'ServeCurrentProject = reahl.webdev.commands:ServeCurrentProject'    ],
                 },
    extras_require={u'pillow': [u'pillow>=2.5,<2.5.999']}
)
