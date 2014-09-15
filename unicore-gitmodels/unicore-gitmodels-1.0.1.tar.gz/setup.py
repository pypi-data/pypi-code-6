from setuptools import setup, find_packages


setup(
    name='unicore-gitmodels',
    version='1.0.1',
    description='Definition of models used for python-gitmodel',
    long_description=
    open('README.rst', 'r').read() +
    open('AUTHORS.rst', 'r').read() +
    open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/unicore-gitmodels',
    packages=find_packages(),
    install_requires=[
        "praekelt-python-gitmodel",
    ],
    include_package_data=True,
    tests_require=[],
    test_suite="setuptest.setuptest.SetupTestSuite",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
