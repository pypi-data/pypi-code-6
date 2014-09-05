from setuptools import setup, find_packages

import bosunplugins

# reqs is a list of requirements
reqs = []

# load README.md
with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='bosunplugins',
    version=bosunplugins.__version__,
    author=bosunplugins.__author__,
    description='Plugin framework for Bosun and Crowsnest, of http://www.crowsnest.io',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=reqs,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
