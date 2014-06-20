from distutils.core import setup

setup(
    name='wsgi-seo-iframe',
    version='0.1.0',
    author='Tiago Queiroz',
    author_email='contato@tiago.eti.br',
    packages=['wsgi_seo_iframe'],
    url='http://github.com/belimawr/wsgi_seo_iframe',
    license='LICENSE.txt',
    description='WSGI middleware for replacing iframes by their html content, allowing them to be crowled by search engines',
    long_description=open('README.rst').read(),
    install_requires=[
        "wsgi-content-modifier",
        "werkzeug",
        "pyquery",
        "selenium",
    ],
)
