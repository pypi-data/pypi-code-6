from distutils.core import setup

setup(
    name='gooimage',
    version='0.0.1',
    author='David',
    author_email='davidyen1124@gmail.com',
    description='Search google images in Python',
    long_description=open('README.md').read(),
    license=open('LICENSE').read(),
    keywords='google image search',
    url='https://github.com/davidyen1124/Google-Image',
    packages=['gooimage'],
    install_requires=[
        'requests==2.4.3',
    ],
)
