__author__ = 'assadmahmood'

from setuptools import setup

setup(
    name = 'asposecloud',
    packages = ['asposecloud', 'asposecloud.barcode', 'asposecloud.cells', 'asposecloud.email', 'asposecloud.ocr',
                'asposecloud.pdf', 'asposecloud.slides', 'asposecloud.tasks', 'asposecloud.words'],
    version = '1.0.0',
    description = 'Aspose Cloud SDK for Python allows you to use Aspose API in your Python applications',
    author='Assad Mahmood Qazi',
    author_email='assadvirgo@gmail.com',
    url='https://github.com/asposeforcloud/Aspose_Cloud_SDK_For_Python/tree/revamp',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
