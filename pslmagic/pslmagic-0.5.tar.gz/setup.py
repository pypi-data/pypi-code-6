from distutils.core import setup

with open('README') as f:
    long_description = f.read()


setup(
    name = 'pslmagic',
    packages = ['pslmagic'], # this must be the same as the name above
    version = '0.5',
    description = 'IPython magic for ParselTongue',
    long_description = long_description,
    author = 'Todd Iverson',
    author_email = 'tiverson@smumn.edu',
    url = 'https://github.com/yardsale8/pslmagic',   # use the URL to the github repo
    download_url = 'https://github.com/yardsale8/pslmagic/tarball/0.5', # I'll explain this in a second
    keywords = ['ParselTongue', 'IPython extension', 'IPython magic'], # arbitrary keywords
    classifiers = ["Development Status :: 3 - Alpha"],
)
