from setuptools import setup
setup(
    name=u'reahl-component',
    version='3.0.0',
    description=u'The component framework of Reahl.',
    long_description=u"Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nReahl-component is the component that contains Reahl's component framework.\n\nSee http://www.reahl.org/docs/3.0/tutorial/gettingstarted.d.html for installation instructions. ",
    url=u'http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.component', 'reahl.messages', 'reahl.component_dev'],
    py_modules=[u'setup'],
    include_package_data=False,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl', 'reahl.messages'],
    install_requires=['six', 'Babel>=1.3,<1.3.9999', 'python-dateutil>=2.2,<2.2.999', 'decorator>=3.4,<3.4'],
    setup_requires=[],
    tests_require=['reahl-tofu>=3.0,<3.1', 'reahl-stubble>=3.0,<3.1'],
    test_suite=u'reahl.component_dev',
    entry_points={
        u'reahl.translations': [
            u'reahl-component = reahl.messages'    ],
        u'reahl.component.databasecontrols': [
            u'NullDatabaseControl = reahl.component.dbutils:NullDatabaseControl'    ],
        u'reahl.eggs': [
            u'Egg = reahl.component.eggs:ReahlEgg'    ],
        u'console_scripts': [
            u'reahl-control = reahl.component.prodshell:ProductionCommandline.execute_one'    ],
        u'reahl.component.prodcommands': [
            u'CreateDBUser = reahl.component.prodshell:CreateDBUser',
            u'DropDBUser = reahl.component.prodshell:DropDBUser',
            u'CreateDB = reahl.component.prodshell:CreateDB',
            u'DropDB = reahl.component.prodshell:DropDB',
            u'BackupDB = reahl.component.prodshell:BackupDB',
            u'RestoreDB = reahl.component.prodshell:RestoreDB',
            u'BackupAllDB = reahl.component.prodshell:BackupAllDB',
            u'RestoreAllDB = reahl.component.prodshell:RestoreAllDB',
            u'SizeDB = reahl.component.prodshell:SizeDB',
            u'RunJobs = reahl.component.prodshell:RunJobs',
            u'CreateDBTables = reahl.component.prodshell:CreateDBTables',
            u'DropDBTables = reahl.component.prodshell:DropDBTables',
            u'MigrateDB = reahl.component.prodshell:MigrateDB',
            u'ListConfig = reahl.component.prodshell:ListConfig',
            u'CheckConfig = reahl.component.prodshell:CheckConfig',
            u'ListDependencies = reahl.component.prodshell:ListDependencies'    ],
                 },
    extras_require={}
)
