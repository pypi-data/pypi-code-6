from distutils.core import setup

setup(name='scarsdale-property-inquiry',
    author='Thomas Levine',
    author_email='_@thomaslevine.com',
    description='Inquire about Scarsdale properties',
    url='https://github.com/tlevine/scarsdale-property-inquiry.git',
    classifiers=[
        'Intended Audience :: Developers',
    ],
    packages=['scarsdale_property_inquiry'],
    scripts=['bin/scarsdale-property-inquiry'],
    install_requires = [
        'requests>=2.1',
        'randua>=0.0.1',
        'randomsleep>=0.1',
        'lxml',
        'pickle_warehouse>=0.0.18',
        'dataset>=0.5.2',
        'PyMySQL>=0.6.2',
        'jumble>=0.0.1',
    ],
    tests_require = ['nose'],
    version='0.4.0',
    license='AGPL',
)
