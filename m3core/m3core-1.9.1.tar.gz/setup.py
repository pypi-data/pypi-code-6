from setuptools import setup
setup(
    name = "m3core",
#    package_dir={ '': '${CMAKE_CURRENT_SOURCE_DIR}' },
    packages = ["m3", "m3rt"],
    version = "1.9.1", 
    description = "Python bindings for the M3 real time control software",
    author = "Meka Robotics LLC",
    license='GNU-Lesser',
    author_email = "info@mekabot.com",
    url = "http://mekabot.com",
)

#TODO : use version='${PACKAGE_VERSION}',
