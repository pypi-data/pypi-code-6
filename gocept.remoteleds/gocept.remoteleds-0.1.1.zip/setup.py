import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='gocept.remoteleds',
    version='0.1.1',
    url='https://bitbucket.org/gocept/gocept.remoteleds',
    license='MIT',
    description='Can speak to an Arduino and set color of connected LEDs.',
    author='Daniel Havlik, Florian Pilz and Oliver Zscheyge',
    author_email='dh@gocept.com',
    long_description=(read('README.rst')
                      + '\n\n' +
                      'Detailed Documentation\n'
                      '**********************'
                      + '\n\n' +
                      read('CHANGES.rst')
                      ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: C',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
    ],
    keywords='arduino led adafruit neopixel',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['gocept'],
    include_package_data=True,
    install_requires=[
        'pyserial',
        'requests',
        'setuptools',
    ],
    entry_points = {
        'console_scripts': [
            'remoteleds = gocept.remoteleds.discovery:main',
        ]
    },
    zip_safe=False,
)
