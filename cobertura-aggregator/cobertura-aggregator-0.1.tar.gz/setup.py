"""CoberturaAggregator setup"""
from setuptools import setup, find_packages
setup(
    name="cobertura-aggregator",
    version="0.1",
    packages=find_packages(),
    license="Creative Commons Attribution-Noncommercial-Share Alike license",
    author="Juan Gutierrez",
    description="Cobertura folder coverage aggregator",
    url="https://github.com/juannyg/cobertura_aggregator/",
    install_requires=[
        "tabulate>=0.7.2",
        "simplejson>=3.6.0",
        "cli-tools>=0.2.5"
    ],
    entry_points={
        "console_scripts": [
            "cobertura_agg = cobertura_aggregator.run:run.console"
        ]
    }
)
