from setuptools import setup
from djrillcelery import __version__

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="djrillcelery",
    version=__version__,
    description='Mandrill transactional email for Django in conjunction with Celery',
    keywords="django, mailchimp, mandrill, email, email backend, djrill",
    author="Jannis Gebauer <ja.geb@me.com>",
    author_email="ja.geb@me.com",
    url="https://github.com/jayfk/DjrillCelery/",
    license="BSD License",
    packages=["djrillcelery"],
    zip_safe=False,
    install_requires=["djrill", "celery"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    long_description=long_description,
)
