try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



setup(
    name = 'latch',
    version = '1.0.0',
    description = 'latch SDK',
    author='Eleven Paths',
    author_email='latch-help@support.elevenpaths.com',
    url='https://github.com/ElevenPaths/latch-sdk-python',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    py_modules = ['latch']
)
