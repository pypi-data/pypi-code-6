import mongosion

test():
	print 'make sure pymongo has installed and mongodb is running'

	# get session ( if null, create it )
	data = mongosion.get('session_id')
	# save session
	mongosion.save( data['_id'], { 'uid':'user id', 'status':'forbidden', 'isLogin':False })
	# delete expired
	mongosion.expired()

	if mongosion.exist( session_id ):
		print session_id + ' session is exist!'	
	else:
		print session_id + ' not exist'

test()