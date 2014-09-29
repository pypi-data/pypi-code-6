#####################################################################################################################
#											HASHTAG.py - HashTagging for dummies									#
#####################################################################################################################
import DBConnectionHandler as dbcon
import bisect
from sets import Set

def UpdateTagValue(cur,data,tagList):
	booleanMap = checkIfTagsExists(cur,tagList)
	for (item,tag) in zip(booleanMap,tagList):
		print item,tag
		if item:
			cur.execute("SELECT data FROM tagStore WHERE tag=%s",[tag])
			commitdata = cur.fetchone()
			commitdata = commitdata["data"]
			commitdata,duplicate = lexiographicAdd(data,commitdata)
			if(duplicate != False):
				cur.execute("UPDATE tagStore SET data='"+str(commitdata)+"' WHERE tag='"+str(tag)+"'")

		else:
			createTag(cur,tag,data)
	# dbcon.closeCon()

# cur.execute("Insert INTO tagStore VALUES('java','2213,342,345345');")
# cur.execute("SELECT * FROM tagStore")
# print cur.fetchall()

#**************************************************#

def checkIfTagsExists(cur,tagList):
	booleanMap=[]
	for tag in tagList:
		cur.execute("SELECT * FROM tagStore WHERE tag=%s",[tag])
		if cur.fetchall() ==():
			booleanMap.append(False)
		else:
			booleanMap.append(True)
	print booleanMap
	return booleanMap

#**************************************************#

def createTag(cur,tag,data):
	cur.execute("INSERT INTO tagStore (tag,data) VALUES (%s,%s)",[tag,data])

#**************************************************#

def lexiographicAdd(data,commitdata):
	Lcommitdata = commitdata.split(",")
	print Lcommitdata
	pos = bisect.bisect(Lcommitdata,data)
	if Lcommitdata[pos-1] == data:
		return commitdata,False
	else:
		bisect.insort(Lcommitdata, data) #Inserting data into sorted Lcommitdata
		#print Lcommitdata
		commitdata = ",".join(Lcommitdata)
		return commitdata,True

#**************************************************#

#### DELETE Functions ####

def DeleteTag(cur, tagList):

	booleanMap = checkIfTagsExists(cur, tagList)

	for (item,tag) in zip(booleanMap, tagList):
		
		print item, tag

		if item:
			cur.execute("DELETE FROM tagStore WHERE tag=%s", [tag])
		
		else:
			continue

#**************************************************#

def DeleteValue(cur, dataSegment):

	cur.execute("SELECT tag,data FROM tagStore WHERE data LIKE '%"+ str(dataSegment) +"%'")

	rows = cur.fetchall()

	for row in rows:
		print row
		datastring = row['data']
		tag = row['tag']
		newdatastring = lexiographicDelete(dataSegment,datastring)
		print "\n",newdatastring
		cur.execute("UPDATE tagStore SET data='"+str(newdatastring)+"' WHERE tag='"+str(tag)+"'")

#**************************************************#

def DeleteValueByTags(cur, dataSegment, tagList):

	booleanMap = checkIfTagsExists(cur,tagList)

	for (item,tag) in zip(booleanMap,tagList):
		print item,tag
		if item:
			cur.execute("SELECT data FROM tagStore WHERE tag='"+str(tag)+"' AND data LIKE '%"+ str(dataSegment) +"%'")
			commitdata = cur.fetchone()
			commitdata = commitdata["data"]
			commitdata = lexiographicDelete(dataSegment, commitdata)
			cur.execute("UPDATE tagStore SET data='"+str(commitdata)+"' WHERE tag='"+str(tag)+"'")
		else:
			continue

#**************************************************#

def lexiographicDelete(data,commitdata):
	Lcommitdata = commitdata.split(",")
	print Lcommitdata
	
	position = bisect.bisect_left(Lcommitdata, data)
	
	if Lcommitdata[position] == data:
		del Lcommitdata[position]

	print Lcommitdata
	
	commitdata = ",".join(Lcommitdata)
	
	return commitdata


# UpdateTagValue("cdivandhya1", ["python","java"])
# UpdateTagValue("cdivandhya2", ["python","java"])
# UpdateTagValue("cdivandhya3", ["python","ruby"])
# UpdateTagValue("cdivandhya4", ["ruby","java"])
# UpdateTagValue("cdivandhya5", ["python","java","ruby"])
#DeleteTag(["php","java"]) #Delete entire Rows that contains tags in the list
#DeleteValue("cdivandhya") # Search for "rahul" (dataSegment) in data and remove it from the string
#DeleteValueByTags("cdivandhya", ["java"])

#end of file