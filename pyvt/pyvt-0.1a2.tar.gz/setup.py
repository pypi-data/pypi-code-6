from setuptools import setup, find_packages

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

__version__ = None
exec(open('pyvt/_version.py').read())  # load the actual __version__

setup(
    name='pyvt',
    version=__version__,
    maintainer='Arman Noroozian',
    maintainer_email='arman.noroozian.developer@gmail.com',
    url='https://github.com/anoroozian/pyvt',
    description='Python VirusTotal Private API 2.0 Implementation.',
    long_description=read_md('README.md'),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords='virustotal api private',
    # py_modules=['__init__', '_version'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    tests_require=['nose', 'coverage'],
    zip_safe=False,
    test_suite='nose.collector',
    # packages=find_packages(exclude=['tests', 'tests.*']),
    # setup_requires=[],
    # install_requires=[],
    # data_files=[],
    # scripts=[],
    # **extra_kwargs
)


