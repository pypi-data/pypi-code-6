from setuptools import setup, find_packages


setup(
    name="django-location-picker",
    version='0.1.0',
    url="https://github.com/jamesfoley/django-location-picker",
    author="James Foley",
    author_email="jamesfoley@onespacemedia.com",
    platforms=["any"],
    packages=find_packages(),
    description='A location picker field for the Django admin',
    install_requires=[
        'django',
        'psycopg2',
        'django-suit',
        'django-optimizations',
        'Pillow',
        'django-reversion',
        'django-usertools',
        'django-historylinks',
        'django-watson',
        'django-extensions',
        'Werkzeug',
        'raven'
    ],
)
