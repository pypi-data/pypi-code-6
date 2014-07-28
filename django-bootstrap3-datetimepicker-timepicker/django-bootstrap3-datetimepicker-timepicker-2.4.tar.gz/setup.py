from setuptools import setup


setup(
    name='django-bootstrap3-datetimepicker-timepicker',
    packages=['bootstrap3_datetime_time',],
    package_data={'bootstrap3_datetime': ['static/bootstrap3_datetime_time/css/*.css', 
                                          'static/bootstrap3_datetime_time/js/*.js',
                                          'static/bootstrap3_datetime_time/js/locales/*.js',]},
    include_package_data=True,
    version='2.4',
    description='Bootstrap3 compatible datetimepicker and timepicker for Django projects.',
    long_description=open('README.rst').read(),
    author='Josh Roy',
    author_email='joshnroy@gmail.com',
    url='https://github.com/joshnroy/django-bootstrap3-datetimepicker',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
