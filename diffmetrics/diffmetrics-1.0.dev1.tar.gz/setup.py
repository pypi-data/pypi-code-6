from setuptools import setup, find_packages

setup(
    name='diffmetrics',
    version='1.0.dev1',
    description='Diff tool for code metrics',
    author='Neal Finne',
    author_email='neal@nealfinne.com',
    url='https://bitbucket.org/nfinne/diffmetrics',
    packages=find_packages(),
    install_requires=['termcolor', 'radon', 'enum34', 'flake8', 'pep8'],
    entry_points={
        'console_scripts': ['diffmetrics = diffmetrics:main']
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
