from setuptools import setup


setup(
    name="expectpy",
    version="0.0.1",
    author="takahiro iwatani",
    author_email="taka.05022002@gmail.com",
    url="https://github.com/float1251/expectpy",
    packages=["expectpy"],
    license="MIT",
    test_suite="expectpy.test",
    classfilters=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License"
    ]
)
