from setuptools import setup


setup(
    name='django-setmagic',
    version='0.1.2',
    author='Evandro Myller',
    author_email='emyller@7ws.co',
    description='Magically editable settings for winged pony lovers',
    url='https://github.com/7ws/django-setmagic',
    install_requires=[
        'django >= 1.5',
    ],
    packages=['setmagic'],
    keywords=['django', 'settings'],
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
