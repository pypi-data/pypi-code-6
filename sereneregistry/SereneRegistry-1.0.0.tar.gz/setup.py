from distutils.core import setup

setup (
    name = 'SereneRegistry',
    version = '1.0.0',
    py_modules = ['SereneRegistry'],
    url = 'https://github.com/SerenitySoftwareLLC/serene-registry',
    author = 'Ryan Vennell',
    author_email = 'ryan.vennell@gmail.com',
    description = 'A simple, non-persistent, key-value registry in memory.',
    license = open('LICENSE', 'r').read(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ]
)
