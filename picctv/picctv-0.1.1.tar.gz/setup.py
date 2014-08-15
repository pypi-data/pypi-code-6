import os
from setuptools import setup, find_packages

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print(
        "warning: pypandoc module not found, "
        "could not convert Markdown to RST"
    )
    read_md = lambda f: open(f, 'r').read()

README = read_md('README.md')

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='picctv',
    version='0.1.1',
    packages=find_packages('src', exclude=('tests',)),
    package_dir={'': 'src'},
    include_package_data=True,
    license='proprietary',
    entry_points={
        'console_scripts': ['picctv = picctv.picctv:main']
    },
    description='CCTV for the RaspberryPi & Camera Module.',
    long_description=README,
    author='Richard O\'Dwyer',
    author_email='richard@richard.do',
    url='https://github.com/richardasaurus/pi-cctv',
    zip_safe=True,
    install_requires=[
        'picamera>=1.7',
        'Pillow>=2.5.2',
        'docopt>=0.6.2',
        'pytest>=2.6.1',
        'pypandoc',
    ]
)
