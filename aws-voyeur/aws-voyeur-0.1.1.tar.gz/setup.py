from setuptools import setup


setup(
    name='aws-voyeur',
    version='0.1.1',
    url='https://github.com/texastribune/aws-voyeur',
    license='BSD',
    author='Chris Chang',
    author_email='cchang@texastribune.org',
    description='List AWS inventory',
    long_description=open('README.md').read(),
    py_modules=['voyeur'],
    entry_points={
        'console_scripts': [
            'voyeur = voyeur:main',
        ],
    },
    install_requires=[
        'boto',
        'tabulate',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
