import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

packages = [
    'drift',
    'drift.content',
    'drift.contrib',
    'drift.contrib.flatpages',
    'drift.contrib.versionedpages',
]

requires = []

setup(
    name='drift',
    version='0.0.4', #content.__version__,
    description='Make editing content directly easier for CMS authors and users.',
    long_description=README,
    author='Albert O\'Connor',
    author_email='info@albertoconnor.ca',
    url='https://bitbucket.org/amjoconn/drift',
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
