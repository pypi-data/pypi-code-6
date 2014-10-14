from setuptools import setup

setup(
    name='Beetle-Image-Compressor',
    version='0.1.0',
    author='Esben Sonne',
    author_email='esbensonne+code@gmail.com',
    description='Auto image compressor for Beetle',
    url='https://github.com/cknv/beetle-image-compressor',
    license='MIT',
    packages=[
        'beetle_image_compressor'
    ],
    classifiers=[
        'Environment :: Plugins',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',

    ],
    install_requires=[
        'Pillow',
    ],
)
