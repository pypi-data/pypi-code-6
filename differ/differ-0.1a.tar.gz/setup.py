from setuptools import setup, find_packages

version = '0.1a'


setup(
    name='differ',
    version=version,
    packages=find_packages(),
    url='',
    license='BSD License',
    author='Samuele Santi',
    author_email='redshadow@hackzine.org',
    description='',
    long_description='',
    install_requires=[],
    # tests_require=tests_require,
    # test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: BSD License',

        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',

        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    package_data={'': ['README.md', 'LICENSE']},
    include_package_data=True,
    zip_safe=False)
