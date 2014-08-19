from setuptools import setup

setup(
    version='1.0',
    name = "craption",
    packages = ['craption'],
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
)
