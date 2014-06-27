from distutils.core import setup

setup(
	name="securenet",
	version="0.1.0",
	description="SecureNet Python Library",
	author="SecureNet",
	author_email="richard@richardstanford.com",
	url="http://www.securenet.com/",
	packages=["securenet"],
	install_requires=["requests >= 2.0"],
)
