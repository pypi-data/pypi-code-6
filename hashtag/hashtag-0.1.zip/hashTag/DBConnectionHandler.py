#####################################################################################################################
#											HASHTAG.py - HashTagging for dummies									#
#####################################################################################################################

##	IMPORT SECTION	##																								#

#####################################################################################################################
##	GLOBAL DECLARATION SECTION	##																					#

db=None

#####################################################################################################################
#
# Function Definition to start a database connection to an existing database(mysql,postgresql)
# or a new database(sqlite 3).
#

def connectDB(db_type="", db_host_name="", db_name="", db_username="", db_password=""):
	
	global db

	## MYSQL CONNECTION BLOCK ##																					#
	if db_type == "mysql":
		import MySQLdb
		db = MySQLdb.connect(db_host_name, db_username, db_password, db_name)
		cur = db.cursor(MySQLdb.cursors.DictCursor)
		db.autocommit(True)
		return cur
	
	## POSTGRESQL CONNECTION BLOCK ##																				#
	elif db_type == "postgresql":
		import psycopg2

		#<<<<<replace with code for postgres
		db = MySQLdb.connect(db_host_name, db_username, db_password, db_name)
		cur = db.cursor(MySQLdb.cursors.DictCursor)
		db.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
		#replace with code for postgres >>>>>
		return cur

	## SQLITE 3 CONNECTION BLOCK ##																					#
	elif db_type == "sqlite3":
		import sqlite3
		db = sqlite3.connect(dbname)
		cur = db.cursor()
		return cur
#
# Function Definition to close a database connection to a connected database.
#

def disconnectDB():
	global db
	try:
		db.close()
		return 0
	except:
		return -1