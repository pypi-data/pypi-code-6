from setuptools import setup, find_packages

setup(
    name='hexlet',
    version='0.0.4',
    description="CLI for hexlet.io",
    long_description=open('README.rst').read(),
    # packages=['towelstuff',],
    license='MIT',
    author="Kirill Mokevnin",
    author_email="mokevnin@gmail.com",
    url="http://hexlet.io",
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'requests',
        'responses',
        'pytest',
        'python-i18n==0.3.0',
        'click==2.2',
        'purl'
    ],
    entry_points = {
        'console_scripts': [
            # 'hexlet=hexlet.cli:main',
            'hexlet-lesson=hexlet.lesson_cli:main'
            ],
    },
    package_data = {'hexlet': ['locales/*.yml'], 'test': ['fixtures/*']}
)
