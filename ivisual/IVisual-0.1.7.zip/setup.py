from distutils.core import setup

setup(
    name='IVisual',
    version='0.1.7',
    author='John Coady',
    author_email='johncoady@shaw.ca',
    packages=['ivisual', 'ivisual.test'],
    package_data={'ivisual': ['data/*.js']},
    url='http://pypi.python.org/pypi/IVisual/',
    license='LICENSE.txt',
    description='VPython visual inline for IPython Notebook',
    long_description=open('README.txt').read(),
    classifiers=[
          'Framework :: IPython',
    ],
)