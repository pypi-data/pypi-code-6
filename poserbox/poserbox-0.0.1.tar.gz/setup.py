from setuptools import setup, find_packages
import poserbox


setup(
    name='poserbox',
    version=poserbox.__version__,
    description="Run sandboxed Poser instance from a python application.",
    long_description=open("README.md").read(),
    url='http://github.com/ziadsawalha/poserbox',
    license=open("LICENSE").read(),
    author=poserbox.__author__,
    author_email='ziad@sawalha.com',
    packages=find_packages(exclude=('tests',)),
    package_data={'': ['LICENSE', '*.md']},
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Testing'
    ],
    tests_require=["nose>=0.10", "poser>=2.0.0"],
    test_suite="nose.collector",
    entry_points={
        'nose.plugins.0.10': [
            'poserbox = poserbox.nose_plugin:PoserBoxPlugin',
        ],
    }
)
