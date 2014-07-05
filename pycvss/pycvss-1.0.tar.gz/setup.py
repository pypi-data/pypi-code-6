try:
    from setuptools import setup
    test_extras = {
        'test_suite': 'pycvss.test',
    }
except ImportError:
    from distutils.core import setup
    test_extras = {}


setup(
    name='pycvss',
    version='1.0',
    author='attwad',
    author_email='tmusoft@gmail.com',
    description=(
        'Cvss manipulation library to easily compute scores.'),
    long_description=open('README.rst').read(),
    url='https://github.com/attwad/pycvss',
    platforms='any',
    packages=[
        'pycvss',
        'pycvss.test',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries',
    ],
    **test_extras
)
