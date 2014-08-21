from setuptools import setup, find_packages


setup(
    name='mpw',
    version='0.1',
    author='Stefan Scherfke',
    author_email='stefan at sofa-rockers.org',
    description='A Python implementation of the Master Password algorithm.',
    long_description='\n\n'.join(
        open(f, 'rb').read().decode('utf-8')
        for f in ['README.txt', 'CHANGES.txt', 'AUTHORS.txt']),
    url='https://bitbucket.org/ssc/mpw',
    license='MIT License',
    install_requires=[
        'click',
        'pyperclip',
        'scrypt',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        mpw = mpw.cli:main
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Security',
    ],
)
