from setuptools import setup


def listify(filename):
    return filter(None, open(filename, 'r').read().strip('\n').split('\n'))

setup(
    name="txmako",
    version="0.1",
    url='http://github.com/calston/txmako',
    license='MIT',
    description="A network mutex service for distributed environments.",
    long_description=open('README.rst', 'r').read(),
    author='Colin Alston',
    author_email='colin.alston@gmail.com',
    packages=[
        "txmako",
    ],
    include_package_data=True,
    install_requires=listify('requirements.txt'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)
