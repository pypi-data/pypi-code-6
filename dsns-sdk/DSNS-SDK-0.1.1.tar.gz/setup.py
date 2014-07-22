from distutils.core import setup

setup(
    name='DSNS-SDK',
    version='0.1.1',
    author='Hari Kishan',
    author_email='hari.kishan@delhivery.com',
    packages=['dsns'],
    url='https://github.com/harkishan81001/dsns-sdk',
    #download_url = 'https://github.com/harkishan81001/dsns-sdk/tarball/0.1'
    license='LICENSE.txt',
    description='DSNS-SDK to interact with Delhivery Simpler Notification Service',
    long_description='',
    install_requires=[
        "Django >= 1.4",
    ],
)
