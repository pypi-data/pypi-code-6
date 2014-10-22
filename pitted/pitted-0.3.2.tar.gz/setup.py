from setuptools import setup, find_packages
import glob
setup(
    name = "pitted",
    version = "0.3.2",
    packages = find_packages(),
    package_data  = {
        "pitted" : ['gnar/*']
    },
    scripts = glob.glob('bin/*py'),
    zip_safe = False,

    description = "Get pitted, so pitted.",
    author = "kortox",
    author_email = "kortox@gmail.com",
    license = "MIT",
    keywords = "pitted drop in get so",
    url = "https://github.com/kortox/pitted",
)
