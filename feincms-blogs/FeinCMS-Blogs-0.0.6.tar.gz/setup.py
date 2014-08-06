from setuptools import setup
import blogs

setup(
    name='FeinCMS-Blogs',
    version=blogs.__version__,
    packages=['blogs', 'blogs.templatetags'],
    license='BSD',
    description='Multiple blog/article app for Django/FeinCMS.',
    long_description=open('README.rst').read(),
    author='Richard Ward',
    author_email='richard.ward@fah-designs.co.uk',
    url='https://github.com/fah-designs/feincms-blogs',
    install_requires=['django', 'feincms', 'feincms-template-content', 'djapps'],
    test_suite='tests',
    tests_require=['python-dateutil'],
)
