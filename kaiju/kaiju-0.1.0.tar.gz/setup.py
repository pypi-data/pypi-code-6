import setuptools

setuptools.setup(
    name="kaiju",
    version="0.1.0",
    url="http://www.geekie.com.br",
    maintainer="Geekie",
    maintainer_email="geekie@geekie.com.br",
    description="Data analysis framework to log operations and interface with MongoDB.",
    packages=["kaiju"],
    include_package_data=True,
    setup_requires=["setuptools_git>=0.4.2"],
    install_requires=["pymongo"],
)
