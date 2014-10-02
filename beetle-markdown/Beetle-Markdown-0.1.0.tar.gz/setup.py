from setuptools import setup

setup(
    name='Beetle-Markdown',
    version='0.1.0',
    author='Esben Sonne',
    author_email='esbensonne+code@gmail.com',
    description='Makes Beetle do markdown',
    url='https://github.com/cknv/beetle-markdown',
    license='MIT',
    packages=[
        'beetle_markdown'
    ],
    classifiers=[
        'Environment :: Plugins',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup',
    ],
    install_requires=[
        'Markdown',
    ],
)
