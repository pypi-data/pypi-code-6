from distutils.core import setup


setup(
    name="mydupfilekiller",
    packages=["mydupfilekiller"],
    description="A Duplicate File Killer",
    version="1.8",
    author="Wiadufa Chen",
    author_email="wiadufachen@gmail.com",
    url="https://github.com/wiadufachen/mydupfilekiller",
    classifiers=["Programming Language :: Python",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: Apache Software License",
                 "Development Status :: 4 - Beta",
                 "Operating System :: OS Independent",
                 ],
    long_description="""\
    My Duplicate File Killer
    ------------------------

      My first library to find duplicate files. You can invoke the find method to find the duplicate files in the paths.

"""
)
