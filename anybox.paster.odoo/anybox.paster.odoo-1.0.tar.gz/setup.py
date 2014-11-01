from setuptools import setup, find_packages

version = '1.0'

setup(
    name='anybox.paster.odoo',
    version=version,
    description="Paster templates to create an Odoo module or instance using buildout",
    long_description=open('README.rst').read() + open('CHANGES.rst').read(),
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='Odoo, paster',
    author='Anybox',
    author_email='jssuzanne@anybox.fr',
    url='http://anybox.fr',
    license='GPL v3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    namespace_packages=['anybox', 'anybox.paster'],
    zip_safe=False,
    install_requires=[
        'setuptools',
        'PasteScript',
        'Cheetah',
    ],
    entry_points="""
      [paste.paster_create_template]
      odoo_module = anybox.paster.odoo.module:Module
      odoo_instance = anybox.paster.odoo.instance:Instance
    """,
)
