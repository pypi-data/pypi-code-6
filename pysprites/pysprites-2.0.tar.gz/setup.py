from setuptools import setup

setup(
    name="pysprites",
    packages=["pysprites"],
    version="2.0",
    description="A mirco python tools for sprite image, support Photoshop layer data",
    author="Mo Norman",
    author_email="ltaoist6@gmail.com",
    license="MIT",
    url="https://github.com/LTaoist/pysprites",
    keywords="sprite images generator png sprites css psd",
    install_requires=["Pillow>=2.2.2", "psd-tools"],
    long_description=open('README.rst').read(),
    scripts=["pysprites/pysprites"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities"],
)
    
    
    
