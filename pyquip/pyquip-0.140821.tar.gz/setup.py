from distutils.core import setup

setup(
    name='pyquip',
    version='0.140821',
    author='Chris Wilson',
    author_email='support+pyquip@aptivate.org',
    packages=['pyquip'],
    package_data={
        'pyquip': [
            'static/js/jquip/dist/*.js',
            'static/js/jquip/src/*.js',
            'static/js/pyquip/*.js',
        ],
    },
    url='http://github.com/aptivate/pyquip',
    license='LICENSE.txt',
    description='Simple installation and django-assets for jQuip',
    install_requires=[
        "django >= 1.5",
        "django_assets >= 0.10",
    ],
)
