from distutils.core import setup

setup(
    name='IVisual',
    version='0.1.0',
    author='John Coady',
    author_email='johncoady@shaw.ca',
    packages=['ivisual', 'ivisual.test'],
    package_data={'ivisual': ['data/*.js']},
    data_files=[('javascript', ['data/glow.1.0.min.js','data/glowcomm.js'])],
    url='http://pypi.python.org/pypi/IVisual/',
    license='LICENSE.txt',
    description='VPython visual inline for IPython Notebook',
    long_description=open('README.txt').read(),
    install_requires=[
        "IPython >= 2.0.0",
        "Numpy >= 1.8.1",
    ],
)