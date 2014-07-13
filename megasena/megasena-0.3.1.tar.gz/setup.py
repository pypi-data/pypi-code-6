from distutils.core import setup

import megasena

setup(
    name='megasena',
    version=megasena.__version__,
    description='Megasena results parser.',
    author='Bruno Silva',
    author_email='bsilva@gmail.com',
    url='https://github.com/bruno-silva/megasena',
    packages=['megasena'],
    install_requires=[
        "beautifulsoup4 == 4.3.2",
    ],
)
