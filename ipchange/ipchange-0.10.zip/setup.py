from setuptools import setup, find_packages
setup(
      name="ipchange",
      version="0.10",
      description="change ubunt static ip address by manipulating the file /etc/network/interfaces, but you must get the root previlege before to call this lib ",
      author="stephon xue",
      author_email = "nobyte@sina.com",
      url="http://sourceforge.net/projects/ubuntustaticipchange/",
      license="BSD",
      platforms = "Linux",
      packages= ["IPChange"],
      classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration"
    ]
)
