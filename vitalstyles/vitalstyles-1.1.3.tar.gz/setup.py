from setuptools import setup, find_packages


setup(
    name = 'vitalstyles',
    description = 'Generate CSS/SASS/LESS documentation with previews using Markdown in comments.',
    version = '1.1.3',
    license = 'BSD',
    author = 'Espen Angell Kristiansen',
    author_email = 'post@espenak.net',
    url = 'https://github.com/appressoas/vitalstyles',
    packages=find_packages(exclude=['manage']),
    install_requires = [
        'setuptools',
        'Markdown',
        'Jinja2',
        'pygments',
    ],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: Python'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
          'vitalstyles-cli = vitalstyles.cli:cli',
        ],
    },
)
