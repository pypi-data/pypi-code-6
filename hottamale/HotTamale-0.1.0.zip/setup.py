from distutils.core import setup

setup(
    name='HotTamale',
    version='0.1.0',
    author='Kyle Ondy',
    author_email='KyleOndy@gmail.com',
    packages=['hottamale'],
    scripts=[],
    url='http://pypi.python.org/pypi/HotTamale/',
    license='LICENSE.txt',
    description='Spiceworks ticket display and notifier.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Flask >= 0.10.1",
    ],
)