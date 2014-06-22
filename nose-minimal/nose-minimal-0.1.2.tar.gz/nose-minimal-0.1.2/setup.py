from distutils.core import setup

setup(
    name = 'nose-minimal',

    version='0.1.2',
    url='https://github.com/gardaud/nose-minimal',
    author='Guillaume Ardaud',
    author_email = 'gardaud@acm.org',
    description = 'A minimal output plugin for the Nose testing framework.',
    license = 'MIT',

    entry_points="""
        [nose.plugins.0.10]
        nose-minimal = noseminimal:NoseMinimal
        """,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
    ],
    requires=['nose']
)
