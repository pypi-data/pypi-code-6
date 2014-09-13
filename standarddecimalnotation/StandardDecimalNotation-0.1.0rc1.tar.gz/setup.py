from distutils.core import setup

setup(
    name='StandardDecimalNotation',
    version='0.1.0rc1',
    author='Shawn David Pringle B.Sc.',
    author_email='sdavidpringle@hotmail.com',
    packages=['standarddecimalnotation', 'standarddecimalnotation.test'],
    data_files=[\
    	('doc/standarddecimalnotation', ['standarddecimalnotation/docs/StandardDecimalNotation.pdf', 'standarddecimalnotation/docs/StandardDecimalNotation.tex']),\
    	\
    	('doc/standarddecimalnotation/singlehtml', [\
	'standarddecimalnotation/docs/singlehtml/index.html',\
	'standarddecimalnotation/docs/singlehtml/objects.inv',\
	'standarddecimalnotation/docs/singlehtml/.buildinfo']),\
	\
	('doc/standarddecimalnotation/singlehtml/_static', [\
	'standarddecimalnotation/docs/singlehtml/_static/file.png',\
	'standarddecimalnotation/docs/singlehtml/_static/underscore.js',\
	'standarddecimalnotation/docs/singlehtml/_static/basic.css',\
	'standarddecimalnotation/docs/singlehtml/_static/searchtools.js',\
	'standarddecimalnotation/docs/singlehtml/_static/up-pressed.png',\
	'standarddecimalnotation/docs/singlehtml/_static/empty',\
	'standarddecimalnotation/docs/singlehtml/_static/pygments.css',\
	'standarddecimalnotation/docs/singlehtml/_static/down.png',\
	'standarddecimalnotation/docs/singlehtml/_static/comment.png',\
	'standarddecimalnotation/docs/singlehtml/_static/up.png',\
	'standarddecimalnotation/docs/singlehtml/_static/sidebar.js',\
	'standarddecimalnotation/docs/singlehtml/_static/comment-close.png',\
	'standarddecimalnotation/docs/singlehtml/_static/minus.png',\
	'standarddecimalnotation/docs/singlehtml/_static/comment-bright.png',\
	'standarddecimalnotation/docs/singlehtml/_static/jquery.js',\
	'standarddecimalnotation/docs/singlehtml/_static/down-pressed.png',\
	'standarddecimalnotation/docs/singlehtml/_static/websupport.js',\
	'standarddecimalnotation/docs/singlehtml/_static/plus.png',\
	'standarddecimalnotation/docs/singlehtml/_static/ajax-loader.gif',\
	'standarddecimalnotation/docs/singlehtml/_static/doctools.js',\
	'standarddecimalnotation/docs/singlehtml/_static/default.css'])],
    scripts=[],    
    url='https://pypi.python.org/pypi/StandardDecimalNotation',
    license='LICENSE.txt',
    description='Numbers in the UI exactly like you learned in school.',
    long_description=open('README.txt').read(),
)
