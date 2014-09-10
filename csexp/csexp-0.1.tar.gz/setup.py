from setuptools import setup

setup(
    name='csexp',
    version='0.1',
    description='Canonical S-expression library',
    author='Dwayne C. Litzenberger',
    author_email='dlitz@dlitz.net',
    #packages=[],
    py_modules=['csexp'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
    ],
    url='https://github.com/dlitz/python-csexp',
    long_description='''\
Library for generating and parsing SPKI canonical s-expressions

See http://people.csail.mit.edu/rivest/Sexp.txt for a description of the
encoding.
''',
)
