from setuptools import setup

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    "Programming Language :: Python",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django'
]

description = "".join((
    "Django commands for reporting code statistics (Classes, KLOCs, etc) from your django project.",
    "Reporting Ruby on Rails' rake stats like stats."
))

setup(
    author='Keita Oouchi',
    author_email='keita.oouchi@gmail.com',
    url='https://github.com/keitaoouchi/django-matome',
    name='django-matome',
    version='0.0.1',
    packages=['matome', 'matome.management', 'matome.management.commands'],
    license='BSD License',
    classifiers=classifiers,
    description=description,
    install_requires=[
        'Django>=1.4',
    ],
    # Packaging options:
    zip_safe=False,
    include_package_data=True
)
