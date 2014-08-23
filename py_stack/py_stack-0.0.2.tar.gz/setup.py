from distutils.core import setup

from py_stack import VERSION

version = ".".join([str(v) for v in VERSION])

setup(
    name='py_stack',
    version=version,
    description='Stack Utilities',
    author='Wojtek Matyskiewicz',
    author_email='wojetk@matyskiewicz.com',
    url='https://github.com/wmatyskiewicz/py-stack/',
    keywords = ['stack'],
    packages=['py_stack'],
    classifiers=[
        str('Intended Audience :: Developers'),
        str('License :: OSI Approved :: MIT License'),
        str('Programming Language :: Python'),
        str("Programming Language :: Python :: 2.7"),
        str('Topic :: Utilities'),
    ],
)
