from setuptools import setup

import github as validator


package = 'sloth_ci.validators'

setup(
    name=validator.__title__,
    version=validator.__version__,
    author=validator.__author__,
    description='GitHub validator for Sloth CI',
    long_description='GitHub Sloth CI validator that validates the GitHub payload against repo name (obtained from the Sloth app config).',
    author_email='moigagoo@live.com',
    url='https://bitbucket.org/moigagoo/sloth-ci-validators',
    py_modules=['%s.github' % package],
    package_dir={package: '.'},
    install_requires = [
        'sloth_ci>=0.6.3'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )