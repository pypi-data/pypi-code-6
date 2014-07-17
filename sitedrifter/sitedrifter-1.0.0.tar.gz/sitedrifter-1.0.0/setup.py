from distutils.core import setup

VERSION = '1.0.0'

setup(
    name='sitedrifter',
    description="Sitedrifter is a Markdown to HTML converter to build static websites.",
    url='https://github.com/brunobord/sitedrifter/',
    author="Bruno Bord",
    author_email='bruno@jehaisleprintemps.net',
    license="MIT",
    platforms='any',
    version=VERSION,
    install_requires=['Markdown', "Jinja2"],
    scripts=['bin/drift']
)
