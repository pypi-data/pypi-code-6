from distutils.core import setup

setup(
    name='HISpectralModel',
    version='0.1.0',
    author='I. M. Stewart',
    author_email='ims@astro.uni-bonn.de',
    packages=['hispectrum', 'hispectrum.test'],
    url='http://pypi.python.org/pypi/HISpectralModel/',
    license='LICENSE.txt',
    description='Generates model HI spectral profiles.',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy >= 1.6.1",
        "scipy >= 0.9.0",
        "matplotlib >= 1.1.1rc",
    ],
)

