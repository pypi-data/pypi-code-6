from setuptools import setup, find_packages

setup(
    name = "lru_cacher",
    packages = find_packages(),
    version = "1.0.0",
    description = "Least Recently used Cache (LRU Cache) in Python",
    author = "Andrew Nystrom",
    author_email = "AWNystrom@gmail.com",
    url = "https://github.com/AWNystrom/lru_cache",
    keywords = ["lru", "cache", "least", "recently", "used"],
    install_requires = ['doubly_linked_list>=1.0.0'],
    license = "Apache 2.0",
    test_suite = 'test_lru_cache',
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