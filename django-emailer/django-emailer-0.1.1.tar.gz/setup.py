from setuptools import setup


setup(
    name='django-emailer',
    version='0.1.1',
    author='Evandro Myller',
    author_email='emyller@7ws.co',
    description='Template based email sending with SMTP connection management',
    url='https://github.com/7ws/django-emailer',
    install_requires=[
        'django >= 1.5',
    ],
    packages=['emailer'],
    keywords=['django', 'email', 'smtp'],
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
