from setuptools import setup
from bell import __version__


setup(
    name='bell',
    version=__version__,
    author='hit9',
    author_email='wangchao@ele.me',
    description='Realtime anomalous metrics detection, for periodic time series, based on carbon',
    keywords='anomaly outlier timeseries metric carbon',
    license='MIT',
    packages=['bell'],
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/eleme/bell',
    entry_points={
        'console_scripts': ['bell=bell.cli:bootstrap']
    },
    install_requires=[
        'numpy',
        'Flask>=0.10.1',
        'docopt',
        'dateutils',
        'blinker>=1.3',
        'toml.py>=0.1.3',
        'beanstalkc>=0.4.0',
        'ssdb.py>=0.1.4',
        'python-cjson>=1.1.0'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)
