from setuptools import setup

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = ''

setup(
    name='django-viewform',
    version='0.1.0',
    description='Template driven form rendering for django.',
    author='Mikhail Podgurskiy',
    author_email='kmmbvnr@gmail.com',
    url='http://github.com/viewflow/viewform',
    keywords="django",
    packages=['viewform',
              'viewform.templatetags'],
    include_package_data=True,
    zip_safe=False,
    license='LGPLv3',
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    install_requires=[
        'django-tag-parser>=2.0'
    ],
)
