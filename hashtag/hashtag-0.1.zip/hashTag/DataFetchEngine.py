#####################################################################################################################
#											HASHTAG.py - HashTagging for dummies									#
#####################################################################################################################
import DBConnectionHandler as dbcon
import bisect
from sets import Set


def dataFetchByTag(cur,tag):

	cur.execute("SELECT data FROM tagStore WHERE tag=%s",[tag])
	
	data = cur.fetchall()
	data = data[0]["data"]
	
	return data




