
SETUP_INFO = dict(
    name = 'infi.dtypes.hctl',
    version = '0.0.7',
    author = 'Tal Yalon',
    author_email = 'tal.yalon@gmail.com',

    url = 'https://github.com/Infinidat/infi.dtypes.hctl',
    license = 'PSF',
    description = """HCTL-related datatypes in Python""",
    long_description = """HCTL-related datatypes in Python""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [],
    namespace_packages = ['infi', 'infi.dtypes'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [],
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

