from setuptools import setup

setup(
    name='suit_guardian',
    version=__import__('suit_guardian').__VERSION__,
    description='django-guardian support for django-suit',
    author='Felipe Martin',
    author_email='fmartingr@me.com',
    url='http://fmartingr.com',
    packages=['suit_guardian'],
    zip_safe=False,
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: Free for non-commercial use',  # Same as django-suit
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ]
)
