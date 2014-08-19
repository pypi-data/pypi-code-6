from setuptools import setup

setup(
    version='1.0.3',
    name = "craption",
    packages = ['craption'],
    description='Simple screenshot uploader',
    author='Jakob Hedman',
    author_email='jakob@hedman.email',
    maintainer='Jakob Hedman',
    maintainer_email='jakob@hedman.email',
    license='GNU GPLv3',
    url='https://github.com/spillevink/CRAPtion',
    package_dir = {'craption':'craption'},
    package_data = {
        'cod': ['glass.mp3'],
    },
    entry_points = {
        'console_scripts': [
            'craption = craption.cli:dispatch',
        ],
    },
    install_requires = [
        'dropbox',
        'pyperclip',
        'requests',
        'opster',
        'configobj',
    ],
    long_description = open('README.rst').read(),
)
