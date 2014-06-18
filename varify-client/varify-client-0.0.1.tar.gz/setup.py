from setuptools import setup

setup(
    name='varify-client',
    version='0.0.1',
    packages=['varify_client'],
    maintainer='Adam Wenocour',
    maintainer_email='wenocur@email.chop.edu',
    description="an HTTP client and supporting utilities for the Varify API",
    download_url='https://github.com/awenocur/varify_client.git',
    entry_points={
        "console_scripts": ['fetchVCF = varify_client._fetchVCF:runCommandLine']
    },
    url='https://github.com/awenocur/varify_client',
    install_requires=["PyVCF"]
)