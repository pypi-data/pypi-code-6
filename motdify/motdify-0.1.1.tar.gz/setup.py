from distutils.core import setup

setup(
    name = 'motdify',
    version = '0.1.1',
    description = 'Create your motd-script with template variables',
    scripts = ['motdify'],
    packages = ['motdenv'],
    package_dir = { 'motdenv': 'motdenv' },
    install_requires = ['psutil'],
    license = 'MIT',
    url = 'https://github.com/LkSky/motdify',
    long_description = ''
)