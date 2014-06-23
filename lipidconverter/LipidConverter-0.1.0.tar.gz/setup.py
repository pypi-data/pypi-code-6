from distutils.core import setup

setup(
    name='LipidConverter',
    version='0.1.0',
    author='Per Larsson',
    author_email='larsson.r.per@gmail.com',
    packages=['lipid_converter'],
    scripts=['bin/lipid_converter.py'],
    url='http://lipid-converter.appspot.com',
    license='LICENSE.txt',
    description='Useful descripton text',
    long_description=open('README.txt').read(),
    install_requires=['NumPy >= 1.6'],
)

