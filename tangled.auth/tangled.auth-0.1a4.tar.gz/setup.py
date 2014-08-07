from setuptools import setup


setup(
    name='tangled.auth',
    version='0.1a4',
    description='Tangled auth integration',
    long_description=open('README.rst').read(),
    url='http://tangledframework.org/',
    download_url='https://github.com/TangledWeb/tangled.auth/tags',
    author='Wyatt Baldwin',
    author_email='self@wyattbaldwin.com',
    packages=[
        'tangled',
        'tangled.auth',
        'tangled.auth.tests',
    ],
    install_requires=[
        'tangled.web>=0.1a9',
    ],
    extras_require={
        'dev': [
            'tangled.web[dev]>=0.1a9',
        ],
    },
    entry_points="""
    [tangled.scripts]
    auth = tangled.auth.command:Command

    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
