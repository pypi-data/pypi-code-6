from setuptools import setup

setup(
    name="ttd",
    version="0.0.1",
    description="Time Till Done (ttd) is a simple progress bar for your long running Python scripts",
    long_description=file('README.rst').read(),
    author="Jarrod C Taylor",
    author_email="jarrod.c.taylor@gmail.com",
    url="https://github.com/JarrodCTaylor/ttd",
    license="WTFPL",
    py_modules=['ttd'],
    classifiers=[
        "Environment :: Console",
        "Topic :: Terminals",
        "Topic :: System :: Shells"
    ],
    tests_require=["nose"],
    test_suite="nose.collector",
)
