from distutils.core import setup	

setup(
	name='django-active-tab',
	version='0.0.1',
	description='nav decorator for django views',
	author='yangchen',
	author_email='yuhan534@126.com',
	url='https://github.com/jarvys.django-active-tab',
	install_requires=[
		'Django'
	],
	py_modules=['django_active_tab'],
	scripts=[],
	keywords=[
		'Django',
		'decorator',
		'view',
		'utilities'
	]
)

