import setuptools


def readme():
    with open("README.rst") as f:
        return f.read()


setuptools.setup(
    name="test_pypi",
    version="0.4",
    description="Test project to learn how pypi works",
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
    ],
    url="comming.soon",
    author="Emiliano G. Molina",
    author_email="emiliano.g.molina@gmail.com",
    license="MIT",
    packages=["test_pypi"],
    install_requires=[
        "tornado",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False)
