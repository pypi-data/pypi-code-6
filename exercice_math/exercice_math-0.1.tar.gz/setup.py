"""
Setuptools setup file.
"""
from setuptools import setup, find_packages

setup(
    name="exercice_math",
    version="0.1",
    packages=find_packages(),

    # metadata for upload to PyPI
    author="Sebatien Delisle",
    author_email="seb0del@gmail.com",
    description="Exercise de Mathematiques",
    license="GNU GPL v3.0 License",
    keywords="math training",
    url="http://",

    # could also include long_description, download_url, classifiers, etc.

    # entry_points.
    # ex.{"entry_point_group_name": ["script_name = package.module:function",]}
    entry_points={
        'console_scripts': [
            'exercise_math = exercice_math.exercice_math:main'
        ]
    },

    # dependencies
    # ex. install_requires=["setuptools==5.8"]
    # ex. dependency_links=["https://testpypi.python.org/pypi"],
    install_requires=[],
    dependency_links=[],

    # including data files
    # ex.
    # package_data={'': ["*.txt", "*.rst"]},
    package_data={},
)
