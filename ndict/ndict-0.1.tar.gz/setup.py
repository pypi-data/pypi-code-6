from setuptools import setup, find_packages

setup(
    name="ndict",
    version=__import__("ndict").__version__,
    description="Named dict for python based on common dict",
    long_description="Named dict for python based on common dict",
    author="Dmitry Kurbatov",
    author_email="dk@dimcha.ru",
    license="BSD",
    url="https://github.com/jet9/python-ndict",
    py_modules=['ndict'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ]
)
