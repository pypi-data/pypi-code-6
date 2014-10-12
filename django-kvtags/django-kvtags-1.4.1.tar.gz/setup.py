try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-kvtags',
    version='1.4.1',
    description='Extensible key-value tagging for Django',
    author='Yigit Ozen',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'django>=1.5',
        'unicodecsv>=0.9.4',
    ],
    package_data={'kvtags': ['templates/*']},
)
