from setuptools import setup, find_packages

setup(
    name='html2pdf',
    version='0.1',
    description='Wkhtmltopdf wrapper',
    long_description="%s\n\n%s" % (open('README.rst', 'r').read(), open('AUTHORS.rst', 'r').read()),
    author='Luis Fernando Barrera',
    author_email='luisfernando@informind.com',
    license='BSD',
    url='https://bitbucket.org/luisfernando/html2pdf',
    packages=find_packages(),
    dependency_links=[],
    install_requires=[],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
