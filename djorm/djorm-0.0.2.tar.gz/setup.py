from distutils.core import setup

setup(
    name='djorm',
    version='0.0.2',
    description='Lightweight wrapper and helpers around the Django ORM',
    author='Kashif Malik',
    author_email='kashif610@gmail.com',
    py_modules=[
        'djorm',
    ],
    install_requires=[
        'Django==1.6.5',
        'funcy==1.1',
    ],
)
