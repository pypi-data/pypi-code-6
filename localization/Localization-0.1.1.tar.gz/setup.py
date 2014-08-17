from distutils.core import setup

setup(
    name='Localization',
    version='0.1.1',
    author='Kamal Shadi',
    author_email='kamal.shadi85@gmail.com',
    packages=['localization', 'localization.test'],
    scripts=['bin/sample.py'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Miltilateration and triangulation.',
    long_description=open('README.txt').read(),
    install_requires=[
        "SciPy >= 0.14.0",
    ],
)
