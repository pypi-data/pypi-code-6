from setuptools import setup


setup(
    name="expectpy",
    version="0.0.4",
    author="takahiro iwatani",
    author_email="taka.05022002@gmail.com",
    description="assertion library like chai.expect.",
    url="https://github.com/float1251/expectpy",
    packages=["expectpy"],
    license="MIT",
    test_suite="expectpy.test",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License"
    ]
)
