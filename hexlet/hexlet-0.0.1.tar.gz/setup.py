from setuptools import setup, find_packages

setup(
    name='hexlet',
    description="CLI for hexlet.io",
    version='0.0.1',
    # packages=['towelstuff',],
    license='MIT',
    author="Kirill Mokevnin",
    author_email="mokevnin@gmail.com",
    url="http://hexlet.ru",
    # long_description=open('README.txt').read(),
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
