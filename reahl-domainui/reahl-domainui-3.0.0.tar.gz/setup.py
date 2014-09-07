from setuptools import setup
setup(
    name=u'reahl-domainui',
    version='3.0.0',
    description=u'A user interface for reahl-domain.',
    long_description=u'Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nThis Reahl component contains a user interface for some of the domain functionality in reahl-domainui.\n\nSee http://www.reahl.org/docs/3.0/tutorial/gettingstarted.d.html for installation instructions. ',
    url=u'http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.messages', 'reahl.domainui', 'reahl.domainui_dev'],
    py_modules=[u'setup'],
    include_package_data=True,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl', 'reahl.messages'],
    install_requires=['reahl-component', 'reahl-sqlalchemysupport>=3.0,<3.1', 'reahl-web', 'reahl-domain>=3.0,<3.1'],
    setup_requires=[],
    tests_require=['reahl-tofu>=3.0,<3.1', 'reahl-stubble>=3.0,<3.1', 'reahl-dev>=3.0,<3.1', 'reahl-webdev>=3.0,<3.1', 'reahl-dev>=3.0,<3.1', 'reahl-webdev>=3.0,<3.1'],
    test_suite=u'reahl.domainui_dev',
    entry_points={
        u'reahl.translations': [
            u'reahl-domainui = reahl.messages'    ],
        u'reahl.configspec': [
            u'config = reahl.domainuiegg:DomainUiConfig'    ],
        u'reahl.workflowui.task_widgets': [
            u'TaskWidget = reahl.domainui.workflow:TaskWidget'    ],
        u'reahl.eggs': [
            u'Egg = reahl.component.eggs:ReahlEgg'    ],
                 },
    extras_require={}
)
