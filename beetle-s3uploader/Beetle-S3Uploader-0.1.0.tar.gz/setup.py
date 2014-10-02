from setuptools import setup

setup(
    name='Beetle-S3Uploader',
    version='0.1.0',
    author='Esben Sonne',
    author_email='esbensonne+code@gmail.com',
    description='Beetle plugin to upload the site to S3',
    url='https://github.com/cknv/beetle-s3uploader',
    license='MIT',
    packages=[
        'beetle_s3uploader'
    ],
    classifiers=[
        'Environment :: Plugins',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=[
        'boto'
    ]
)
