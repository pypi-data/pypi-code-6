import os

from setuptools import find_packages
from setuptools import setup

version = '0.1'
project = 'kotti_quiz'

install_requires = [
    'Kotti',
],

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

setup(
    name=project,
    version=version,
    description="Quiz Content Type for Kotti",
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "License :: Repoze Public License",
    ],
    keywords='kotti addon',
    author='Sebastian Brass',
    author_email='brass@xo7.de',
    url='https://github.com/sbabrass/kotti_quiz',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[],
    entry_points={
        'fanstatic.libraries': [
            'kotti_quiz = kotti_quiz.fanstatic:library',
        ],
    },
    extras_require={},
    message_extractors={
        'kotti_quiz': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
        ]
    },
)
