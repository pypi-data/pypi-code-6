from setuptools import setup, find_packages


setup(
    name='collective.envlogfile',
    version='1.0.0',
    description='',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='https://github.com/datakurre/collective.envlogfile',
    license='EUPL',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'ZConfig',
    ],
    extras_require={'test': [
    ]},
    entry_points="""
    """,
)
