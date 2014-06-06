from setuptools import setup

setup(
    name='transmedia',
    version=__import__('transmedia').__version__,
    description='utilities for thumbing one\'s nose at intellectual property \
    law (or not)',
    url='https://github.com/jonnystorm/transmedia',
    license='WTFPLv2',
    author='jstorm',
    author_email='the.jonathan.storm@gmail.com',
    setup_requires=['nose>=1.0'],
    include_package_data=True,
    packages=['transmedia', 'transmedia.tests'],
    long_description="""transmedia is a collection of utilities for toying\
    with audio/image conversion (and copyright/trademark law).""",
    classifiers=[
        'License :: Public Domain',  # OSI Rejected :: WTFPLv2
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Other Audience',  # anti-IP zealots, the curious
        'Topic :: Multimedia',
    ],
    keywords='media conversion audio image copyright trademark hogwash',
    install_requires=['setuptools'],
)
