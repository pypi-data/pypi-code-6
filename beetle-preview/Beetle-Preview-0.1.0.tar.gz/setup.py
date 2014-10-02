from setuptools import setup

setup(
    name='Beetle-Preview',
    version='0.1.0',
    author='Esben Sonne',
    author_email='esbensonne+code@gmail.com',
    description='Local test server plugin for Beetle',
    url='https://github.com/cknv/beetle-preview',
    license='MIT',
    packages=[
        'beetle_preview'
    ],
    classifiers=[
        'Environment :: Plugins',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
    install_requires=[
        'watchdog'
    ],
)
