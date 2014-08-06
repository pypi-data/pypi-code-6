import setuptools

setuptools.setup(
    name="radiobabel",
    version="0.1.0",
    url="https://github.com/rehabradio/radiobabel",

    author="Paddy Carey",
    author_email="patrick@rehabstudio.com",
    maintainer="Paddy Carey",
    maintainer_email="patrick@rehabstudio.com",

    description="Interact with a number of online music services using a single unified API.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'soundcloud>=0.4.1',
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
