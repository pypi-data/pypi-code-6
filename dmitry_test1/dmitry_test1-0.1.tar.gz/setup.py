from distutils.core import setup

#files=["things/*"] 
setup(
    name="dmitry_test1",
    version="0.1",
    description="A Simple Package1",
    author="dmitry",
    author_email="mazda266@gmail.com",
    url="http://www.blog.pythonlibrary.org/2012/07/08/python-201-creating-modules-and-packages/",
    packages=["package1"],
    #package_data = {'package1' : files },
    long_description="""Really long text here."""
)
