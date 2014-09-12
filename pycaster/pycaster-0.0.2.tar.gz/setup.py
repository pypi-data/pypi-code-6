from distutils.core import setup

setup(
    name='pycaster',
    version='0.0.2',
    author='Adamos Kyriakou',
    author_email='somada141@gmail.com',
    packages=['pycaster',
              'pycaster.test'],
    package_data={'pycaster.test': ['data/*.*']},
    url='http://pypi.python.org/pypi/pycaster/',
    license='LICENSE.txt',
    description='A Python package which uses VTK to perform ray-casting',
    long_description=open('README.txt').read(),
    install_requires=[
        "vtk >= 5.10.1",
        "fieldpy >= 0.1.5",
        "nose >= 1.3.3",
    ],
)
