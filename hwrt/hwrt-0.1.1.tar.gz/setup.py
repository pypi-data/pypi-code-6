try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'hwrt',
    'version': '0.1.1',
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'packages': ['hwrt'],
    'scripts': ['hwrt/backup.py'],
    'url': 'https://github.com/MartinThoma/hwrt',
    'license': 'MIT',
    'description': 'Handwriting Recognition Tools',
    'long_description': """A tookit for handwriting recognition. It was
    developed as part of the bachelors thesis of Martin Thoma.""",
    'install_requires': [
        "argparse >= 1.2.1",
        "numpy >= 1.8.1",
        "theano >= 0.6.0",
        "nose",
    ],
    'entry_points': {
        'console_scripts': ['hwrt.backup = hwrt:main']
    },
    'keywords': ['HWRT', 'recognition', 'handwriting', 'on-line'],
    'download_url': 'https://github.com/MartinThoma/hwrt',
}

setup(**config)
