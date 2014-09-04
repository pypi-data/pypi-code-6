extensions = [
	# bunch of extensions to be loaded up when web server starts
]

config = {

	'extensions' : {

	},

	# database configuration
	'db' : {
		# 'default' : {
		# 	'driver' : 'mysql',
		# 	'host' : 'localhost',
		# 	'schema' : 'test',
		# 	'user' : 'root',
		# 	'password' : '',
		# },
	},
	
	'log' : {
		# 'level' : 'info',
		# 'format' : '[%(levelname)s] : %(message)s',
		# 'file' : 'app/storage/logs/debug.log'
	},

	'views' : {
		'path' : 'app/views',
	},

	'sessions' : {
		'id_header' : 'glim_session',
		'path' : 'app/storage/sessions',
	},
	
	# app specific configurations
	# reloader: detects changes in the code base and automatically restarts web server
	# debugger: enable werkzeug's default debugger

	'app' : {
		'reloader' : True,
		'debugger' : True,		
	}
}
