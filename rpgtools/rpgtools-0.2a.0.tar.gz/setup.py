from setuptools import setup, find_packages

with open('requirements.txt') as file:
    required = file.read().splitlines()

setup(
    name='rpgtools',
    version='0.2a.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    url='https://github.com/gcavalcante8808/rpgtools',
    license='License :: OSI Approved :: Apache Software License',
    author='Gabriel Abdalla Cavalcante',
    author_email='gabriel.cavalcante88@gmail.com',
    description="""Rpgtools consist in a set of programs/tools usefull for
    RolePlayingGame.""",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
    ],
)