from setuptools import setup, find_packages

setup(
    name='django-chunks2',
    version='2.8',
    description='Keyed blocks of content for use in your Django templates',
    keywords="django metrics",
    #long_description=open('README.md').read(),
    author='Ruslan Popov',
    author_email='ruslan.popov@gmail.com',
    url='https://github.com/RaD/django-chunks',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    install_requires=[
        'easy_thumbnails',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Topic :: Utilities'
    ],
)
