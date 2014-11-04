import setuptools


setuptools.setup(
    name="test_pypi",
    version="0.22",
    description="Test project to learn how pypi works",
    url="",
    author="Emiliano G. Molina",
    author_email="emiliano.g.molina@gmail.com",
    license="MIT",
    packages=["test_pypi", ],
    install_requires=[
        "tornado",
    ],
    zip_safe=False)
