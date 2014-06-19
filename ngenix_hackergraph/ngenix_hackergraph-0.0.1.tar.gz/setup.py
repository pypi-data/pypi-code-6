from distutils.core import setup

setup(
    name='ngenix_hackergraph',
    description="NGENIX graphs in console",
    version='0.0.1',
    url="https://github.com/NGENIX/hackergraph",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    author="NGENIX crew",
    author_email='info@ngeinx.net',
    py_modules=['hackergraph'],
    entry_points={
        'console_scripts': ['hackergraph = hackergraph:main'],
    },
    classifiers = [
        'Environment :: Console'
    ],
)