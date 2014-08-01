from setuptools import setup, find_packages

import imaplib3

setup(
    name="imaplib3",
    version=imaplib3.__version__,
    description="Python IMAP Library",
    # long_desription=(open('README.md').read()),
    url="https://github.com/clara-labs/imaplib3",
    author="Clara",
    license='MIT',
    keywords=["imaplib", "imap"],
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications :: Email :: Post-Office :: IMAP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    use_2to3=True,
)
