from distutils.core import setup

setup(
    name = 'motdify',
    version = '0.1.0',
    description = 'Create your motd-script with template variables',
    scripts = ['motdify'],
    packages = ['motdenv'],
    package_dir = { 'motdenv': 'motdenv' },
    install_requires = ['psutil'],
    license = 'MIT',
    url = 'http://lukas.weissenboeck.at/r/motdify',
    long_description = ''
)