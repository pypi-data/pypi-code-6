from setuptools import setup
setup(
    name='reahl-domain',
    version=u'2.1.2',
    description=u'End-user domain functionality for use with Reahl.',
    long_description=u'Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nThis Reahl component includes functionality modelling user accounts, some simple workflow concepts and more.\n\nSee http://www.reahl.org/docs/current/tutorial/gettingstarted.d.html for installation instructions. ',
    url=u'http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.domain_dev', 'reahl.messages'],
    py_modules=[u'setup'],
    include_package_data=True,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl', 'reahl.messages'],
    install_requires=[u'reahl-component', u'reahl-mailutil', u'reahl-interfaces', u'reahl-sqlalchemysupport>=2.1,<2.2', u'elixir>=0.7,<0.8'],
    setup_requires=[],
    tests_require=[u'reahl-tofu>=2.1,<2.2', u'reahl-stubble>=2.1,<2.2', u'reahl-dev>=2.1,<2.2'],
    test_suite=u'reahl.domain_dev',
    entry_points={
        u'reahl.translations': [
            u'reahl-domain = reahl.messages'    ],
        u'reahl.configspec': [
            u'config = reahl.systemaccountmodel:SystemAccountConfig'    ],
        u'reahl.eggs': [
            u'Egg = reahl.component.eggs:ReahlEgg'    ],
        u'reahl.scheduled_jobs': [
            u'DeferredAction.check_deadline = reahl.workflowmodel:DeferredAction.check_deadline',
            u'UserSession.remove_dead_sessions = reahl.systemaccountmodel:UserSession.remove_dead_sessions'    ],
        u'reahl.persistlist': [
            u'0 = reahl.partymodel:Party',
            u'1 = reahl.systemaccountmodel:SystemAccount',
            u'2 = reahl.systemaccountmodel:UserSession',
            u'3 = reahl.systemaccountmodel:EmailAndPasswordSystemAccount',
            u'4 = reahl.systemaccountmodel:AccountManagementInterface',
            u'5 = reahl.systemaccountmodel:VerificationRequest',
            u'6 = reahl.systemaccountmodel:VerifyEmailRequest',
            u'7 = reahl.systemaccountmodel:NewPasswordRequest',
            u'8 = reahl.systemaccountmodel:ActivateAccount',
            u'9 = reahl.systemaccountmodel:ChangeAccountEmail',
            u'10 = reahl.workflowmodel:DeferredAction',
            u'11 = reahl.workflowmodel:Requirement',
            u'12 = reahl.workflowmodel:Queue',
            u'13 = reahl.workflowmodel:Task'    ],
                 },
    extras_require={}
)
