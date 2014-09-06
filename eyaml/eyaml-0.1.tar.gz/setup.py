from setuptools import setup

setup(
    name='eyaml',
    version='0.1',
    description='Thin Wrapper around PyYAML with env support',
    author='Bryan Marty',
    author_email='bryan@bryanmarty.com',
    license='MIT',
    keywords="yaml env environment",
    url='http://www.bryanmarty.com/',
    packages=['eyaml'],
    install_requires=[
        "PyYAML"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ]
)
