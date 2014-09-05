from setuptools import setup

setup(
    name='sphinxcontrib-visio',
    version='0.9.0',
    author='Yassu',
    packages=['sphinxcontrib'],
    description='Python reStructuredText directive for embedding visio image',
    long_description = (
        'This program provides the directive called visio.\n'
        'Requirements of this program is visio2img, which I made.'
        ),
    url='https://github.com/yassu/sphinxcontrib-visio',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Freeware',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Office/Business'
    ],
    author_email='yassumath@gmail.com',
    license='Apache',
    install_requires=[
        'visio2img'
    ],
    namespace_packages=['sphinxcontrib'],
)
