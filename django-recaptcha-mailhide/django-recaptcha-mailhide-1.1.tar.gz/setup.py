import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-recaptcha-mailhide',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
	install_requires=['pycrypto'],
    license='MIT',  
    description='ReCAPTCHA Mailhide is an app for hiding mails from spammers. To use with Django templates.',
    long_description=README,
    url='https://github.com/bgryszko/django-recaptcha-mailhide',
    author='Bartosz Gryszko',
	author_email='b@gryszko.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)