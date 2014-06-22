try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    
from setuptools import setup, Extension



setup(name="pytinyxml2",
      description="Python wrapper for tinyxml2",
      version="2.1.0",
      author="Wiadufa Chen",
      author_email="wiadufachen@gmail.com",
      url="https://github.com/wiadufachen/pytinyxml2",
      py_modules=['pytinyxml2'],
      ext_modules=[
                    Extension("_pytinyxml2", ['pytinyxml2.i',
                                               "tinyxml2.cpp"],
                              swig_opts=['-c++'])
                    ],
      classifiers=["Programming Language :: Python",
             "Programming Language :: Python :: 3",
             "License :: OSI Approved :: Apache Software License",
             "Development Status :: 4 - Beta",
             "Operating System :: OS Independent",
             ]
)