import setuptools


setuptools.setup(
    name='spandex',
    version='1.1.0',
    description='Do something useful with elasticsearch + logstash.',
    author='Dolph Mathews',
    author_email='dolph.mathews@gmail.com',
    url='http://github.com/dolph/spandex',
    install_requires=['requests', 'pyyaml'],
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['spandex = spandex.cli:main']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
)
