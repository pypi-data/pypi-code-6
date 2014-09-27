from setuptools import setup, find_packages

setup(
    name='collective.runhook',
    version='0.9.5',
    description=(
        'Named instance run script entry points for plone.recipe.zope2instance'
    ),
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='https://github.com/collective/collective.runhook/',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.recipe.zope2instance',
    ],
    extras_require={'test': [
    ]},
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    [plone.recipe.zope2instance.ctl]
    runhook = collective.runhook:runhook
    [collective.runhook]
    whoami = collective.runhook:whoami
    """
)
