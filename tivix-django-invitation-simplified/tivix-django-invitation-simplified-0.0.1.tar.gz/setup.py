from setuptools import setup, find_packages

setup(
    name='tivix-django-invitation-simplified',
    version='0.0.1',
    description='Simple Django app to allow user registration by invitation.',
    author='Joe Carpenter',
    author_email='lungofish@gmail.com',
    maintainer="Sumit Chachra",
    maintainer_email="sumit@tivix.com",
    url='https://github.com/Tivix/django-invitation-simplified',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    zip_safe=False,
    # Tells setuptools to download setuptools_hg before running setup.py so
    # it can find the data files under Hg version control.
)
