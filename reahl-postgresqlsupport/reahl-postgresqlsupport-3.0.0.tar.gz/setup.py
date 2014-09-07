from setuptools import setup
setup(
    name=u'reahl-postgresqlsupport',
    version='3.0.0',
    description=u'Support for using PostgreSQL with Reahl.',
    long_description=u'Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nThis package contains infrastructure necessary to use Reahl with PostgreSQL.\n\nSee http://www.reahl.org/docs/3.0/tutorial/gettingstarted.d.html for installation instructions. ',
    url=u'http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl'],
    py_modules=[u'setup'],
    include_package_data=False,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl'],
    install_requires=['reahl-component>=3.0,<3.1', 'psycopg2>=2.5,<2.5.9999'],
    setup_requires=[],
    tests_require=['reahl-tofu>=3.0,<3.1', 'reahl-stubble>=3.0,<3.1'],
    test_suite=u'tests',
    entry_points={
        u'reahl.component.databasecontrols': [
            u'PostgresqlControl = reahl.postgresqlsupport:PostgresqlControl'    ],
        u'reahl.eggs': [
            u'Egg = reahl.component.eggs:ReahlEgg'    ],
                 },
    extras_require={}
)
