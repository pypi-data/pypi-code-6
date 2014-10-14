from setuptools import setup


with open('README.rst') as f:
    readme = f.read()


setup(
    name='ytrans',
    version='0.1.1',
    packages=['ytrans'],
    url='https://github.com/rkashapov/yandex-translator',
    license='MIT License',
    author='Emmanuel Odeke, Rustam Kashapov',
    author_email='hardtechnik91@gmail.com',
    description='Unoficial client for yandex translator',
    long_description=readme,
    test_suite='run_tests.run_tests',
    zip_safe=False,
    scripts=[
        'ytrans/bin/ytranslate.py',
        'ytrans/bin/ytrans-interactive.py'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
