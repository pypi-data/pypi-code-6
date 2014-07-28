from distutils.core import setup

setup(
    name='HamperCLITest',
    version='0.1.0',
    author='Kiran Panesar',
    author_email='kiransinghpanesar@googlemail.com',
    packages=['hamper'],
    url='https://github.com/MobileXLabs/hamper/',
    license='LICENSE.txt',
    description='A CLI for iOS app provisioning.',
    long_description=open('README.md').read(),
    install_requires=[
      "selenium",
      "docopt",
      "termcolor"
    ],
)