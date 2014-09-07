from setuptools import setup
setup(
    name=u'reahl-sqlalchemysupport',
    version='3.0.0',
    description=u'Support for using SqlAlchemy with Reahl.',
    long_description=u'Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nThis package contains infrastructure necessary to use Reahl with SqlAlchemy or Elixir.\n\nSee http://www.reahl.org/docs/3.0/tutorial/gettingstarted.d.html for installation instructions. ',
    url=u'http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.sqlalchemysupport_dev', 'reahl.sqlalchemysupport'],
    py_modules=[u'setup'],
    include_package_data=False,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl'],
    install_requires=['reahl-component>=3.0,<3.1', 'sqlalchemy>=0.9.2,<0.9.999', 'alembic>=0.6,<0.6.999'],
    setup_requires=[],
    tests_require=['reahl-domain>=3.0,<3.1', 'reahl-dev>=3.0,<3.1', 'reahl-tofu>=3.0,<3.1', 'reahl-stubble>=3.0,<3.1'],
    test_suite=u'reahl.sqlalchemysupport_dev',
    entry_points={
        u'reahl.configspec': [
            u'config = reahl.sqlalchemysupport:SqlAlchemyConfig'    ],
        u'reahl.migratelist': [
            u'0 = reahl.sqlalchemysupport.elixirmigration:ElixirToDeclarativeSqlAlchemySupportChanges'    ],
        u'reahl.eggs': [
            u'Egg = reahl.component.eggs:ReahlEgg'    ],
        u'reahl.persistlist': [
            u'0 = reahl.sqlalchemysupport:SchemaVersion'    ],
                 },
    extras_require={}
)
