try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from mydesire import __version__

setup(
    name='mydesire',
    version=__version__,
    py_modules=['mydesire', 'data'],
    license='MIT License',
    author='dokenzy',
    author_email='dokenzy@gmail.com',
    url='https://github.com/dokenzy/mydesire',
    description='Korean version of loremipsum',
    long_description='Korean version of loremipsum using a section of the article "My Desire" written by Kim koo(or Kim Gu) who was a Korean nationalist politician and independence fighter.(~ wikipedia)',
    keywords=['korean', 'loremipsum', 'My desire', 'Kim koo', 'Kim Gu'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Text Processing :: General'
    ]
)
