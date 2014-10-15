from distutils.core import setup	

setup(
	name='lightpay',
	version='0.0.1',
	description='interface for baidu lightapp pay',
	author='jarvys',
	author_email='yuhan534@126.com',
	url='http://github.com/jarvys/lightpay',
	install_requires=['requests'],
	py_modules=['lightpay'],
	scripts=[],
	keywords=[
		'baidu',
		'lightapp'
	]
)

