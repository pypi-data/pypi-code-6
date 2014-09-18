from setuptools import setup
setup(
    name=u'reahl-web-declarative',
    version='3.0.0',
    description=u'An implementation of Reahl persisted classes using Elixir.',
    long_description=u'Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nSome core elements of Reahl can be implemented for use with different persistence technologies. This is such an implementation based on SqlAlchemy/Elixir.\n\nSee http://www.reahl.org/docs/3.0/tutorial/gettingstarted.d.html for installation instructions. ',
    url=u'http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.webdeclarative', 'reahl.webdeclarative_dev'],
    py_modules=[u'setup'],
    include_package_data=True,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl'],
    install_requires=['reahl-interfaces', 'reahl-sqlalchemysupport>=3.0,<3.1', 'reahl-web', 'reahl-component', 'reahl-domain>=3.0,<3.1'],
    setup_requires=[],
    tests_require=['reahl-tofu>=3.0,<3.1', 'reahl-stubble>=3.0,<3.1', 'reahl-dev>=3.0,<3.1', 'reahl-webdev>=3.0,<3.1'],
    test_suite=u'reahl.webdeclarative_dev',
    entry_points={
        u'reahl.configspec': [
            u'config = reahl.webdeclarative.webdeclarative:WebDeclarativeConfig'    ],
        u'reahl.migratelist': [
            u'0 = reahl.webdeclarative.migrations:RenameRegionToUi',
            u'1 = reahl.webdeclarative.migrations:ElixirToDeclarativeWebDeclarativeChanges'    ],
        u'reahl.eggs': [
            u'Egg = reahl.component.eggs:ReahlEgg'    ],
        u'reahl.persistlist': [
            u'0 = reahl.webdeclarative.webdeclarative:WebUserSession',
            u'1 = reahl.webdeclarative.webdeclarative:SessionData',
            u'2 = reahl.webdeclarative.webdeclarative:UserInput',
            u'3 = reahl.webdeclarative.webdeclarative:PersistedException',
            u'4 = reahl.webdeclarative.webdeclarative:PersistedFile'    ],
                 },
    extras_require={}
)
