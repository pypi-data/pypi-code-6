from setuptools import setup, find_packages


with open('./README.rst') as f:
    long_desc = f.read()


setup(
    name='genscrapeclient',
    version='0.2.2',
    author='Vineet Naik',
    author_email='vineet.naik@kodeplay.com',
    url='http://kodeplay.com',
    license='MIT License',
    description='Client API library for the Genscrape API',
    long_description=long_desc,
    install_requires=["requests-oauthlib==0.4.0"],
    packages=find_packages()
)
