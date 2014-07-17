from distutils.core import setup

setup(
    name='fabric-utils',
    version='0.0.2',
    author='David Saenz Tagarro',
    author_email='david.saenz.tagarro@gmail.com',
    packages=['lib', 'lib.fabric'],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='https://github.com/dsaenztagarro/fabric-utils',
    license='LICENSE.txt',
    description='Fabric utils for deployment management',
    long_description=open('README.txt').read(),
    # install_requires=[
    #     'Django==1.6.2',
    #     'Fabric==1.7.0',
    # ],
)
