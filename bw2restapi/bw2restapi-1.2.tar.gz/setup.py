from setuptools import setup

setup(
    name='bw2restapi',
    version="1.2",
    packages=["bw2restapi", "bw2restapi.tests", "bw2restapi.bin"],
    author="Chris Mutel",
    author_email="cmutel@gmail.com",
    license=open('LICENSE.txt').read(),
    install_requires=["brightway2", "bw2ui", "flask", "docopt"],
    entry_points = {
        'console_scripts': [
            'bw2-restapi = bw2restapi.bin.bw2_restapi:main'
        ]
    },
    url="https://bitbucket.org/cmutel/brightway2-restapi",
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
    ],
)
