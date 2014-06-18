from setuptools import setup
import stack_watcher

setup(
    name='stack-watcher',
    version=stack_watcher.__version__.strip(),
    url='http://dirtymonkey.co.uk/stackoverflow-watcher',
    license='MIT',
    author=stack_watcher.__author__.strip(),
    author_email='matt@dirtymonkey.co.uk',
    description=stack_watcher.__doc__.strip(),
    long_description=open('README.rst').read(),
    keywords='stackoverflow stack overflow watcher monitor api',
    packages=['stack_watcher'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'stack-watcher = stack_watcher.main:main',
        ],
    },
    test_suite='tests',
    tests_require=[
        'py>=1.4.20',
        'pytest>=2.5.2',
    ],
    install_requires=[
        'requests>=2.3.0',
        'docopt>=0.6.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards',
    ],
)
