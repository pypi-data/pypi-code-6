
SETUP_INFO = dict(
    name = 'infi.greeter',
    version = '0.0.1',
    author = 'Tal Yalon',
    author_email = 'yalon@infinidat.com',

    url = 'https://infinigit.infinidat.com/host/greeter',
    license = 'PSF',
    description = """Linux greeter to wrap around /bin/login""",
    long_description = """Linux greeter to wrap around /bin/login""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = ['setuptools', 'npyscreen', 'click', 'infi.traceback'],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = ['greeter = infi.greeter.scripts:main'],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

