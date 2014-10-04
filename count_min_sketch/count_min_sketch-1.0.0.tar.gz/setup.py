from setuptools import setup, find_packages

setup(
    name = "count_min_sketch",
    packages = find_packages(),
    version = "1.0.0",
    description = "A fast Count-Min Sketch data structure.",
    author = "Andrew Nystrom",
    author_email = "AWNystrom@gmail.com",
    url = "https://github.com/AWNystrom/CountMinSketch",
    keywords = ["count", "min", "sketch", "fast"],
    license = "Apache 2.0",
    long_description=open('README.txt').read(),
    classifiers = ["Programming Language :: Python", 
    			   "Programming Language :: Python :: 2.7",
    			   "Programming Language :: Python :: 2",
    			   "License :: OSI Approved :: Apache Software License",
    			   "Operating System :: OS Independent",
    			   "Development Status :: 4 - Beta",
    			   "Intended Audience :: Developers"
    			   ]
	)
