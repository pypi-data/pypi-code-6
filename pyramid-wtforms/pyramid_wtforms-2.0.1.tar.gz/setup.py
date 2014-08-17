try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pyramid_wtforms',
    version='2.0.1',
    packages=['pyramid_wtforms',],
    description='pyramid_wtforms provides bindings for the Pyramid web framework to the WTForms library.',
    author='Evan Nook',
    author_email='evannook@pylabs.net',
    url='https://bitbucket.org/evannook/pyramid_wtforms',
    license='BSD',
    long_description=open('README.txt').read(),
    install_requires = ['pyramid>=1.5', 'wtforms>=2.0,<2.1'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
    ]
)
