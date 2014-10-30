from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    author='Brad Scheppler',
    author_email='brad@tenxer.com',
    description='Automate Pivotal usage with git hooks',
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    keywords='git hook pre-commit prepare-commit-msg',
    license='MIT',
    long_description=readme(),
    name='tenxer_pivotal_git_hooks',
    packages=['tenxer_pivotal_git_hooks'],
    scripts=[
        'bin/tx-pivotal-post-checkout',
        'bin/tx-pivotal-prepare-commit-msg',
    ],
    url='http://github.com/tenXer/tenxer_pivotal_git_hooks',
    version='0.1.2',
    zip_safe=False,
)
