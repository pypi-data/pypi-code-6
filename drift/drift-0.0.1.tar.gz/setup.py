try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'drift',
]

requires = []

setup(
    name='drift',
    version='0.0.1', #content.__version__,
    description='Make editing content directly easier for CMS authors and users.',
    long_description=open('README.rst').read(),
    author='Albert O\'Connor',
    author_email='info@albertoconnor.ca',
    url='https://bitbucket.org/amjoconn/drift',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={},
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
