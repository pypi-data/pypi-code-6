#####################################################################################################################
#											HASHTAG.py - HashTagging for Immortals									#
#####################################################################################################################

import Parser
import Datastore
import TagSearch
import json
import DBConnectionHandler as dbcon
import sets


#**************************************************#

class hashTag:

	def __init__(self, db_type = "sqlite3", db_host_name = None, db_name = "hash_tags", db_username = None, db_password = None):
		
		self.db_type = db_type
		self.db_host_name = db_host_name
		self.db_name = db_name
		self.db_username = db_username
		self.db_password = db_password

		if db_type == "sqlite3":
			self.cur = dbcon.connectDB(db_type)

		elif db_type == "mysql" or db_type == "postgresql":
			
			if db_host_name == None or db_username == None or db_password == None:
				#throw an error : invalid number of parameters passed
				return

			self.cur = dbcon.connectDB(db_type, db_host_name, db_name, db_username, db_password)

	#**************************************************#

	def __del__(self):
		dbcon.disconnectDB();

	#**************************************************#

	def store(self, data_string):
		if len(data_string) == 0:
			msg = {"status" : -1, "message" : "Data string is empty"}
			return json.dumps(msg)

		data_string, tag_list = Parser.parse_tags(data_string)

		if tag_list == None:
			msg = {"status" : -2, "message" : "No tags in supplied data"}
			return json.dumps(msg)

		Datastore.UpdateTagValue(self.cur, data_string,tag_list)

	#**************************************************#

	def storeByTagsList(self, data_string, tag_list):
		if len(data_string) == 0:
			msg = {"status" : -1, "message" : "Data string is empty"}
			return json.dumps(msg)

		if tag_list == None: 
			msg = {"status" : -2, "message" : "No tags in supplied data"}
			return json.dumps(msg)
		tag_list = [tag.strip() for tag in tag_list if len(tag.strip()) != 0]
		Datastore.UpdateTagValue(self.cur,data_string,tag_list)
		print 
		print "*************"
		return tag_list
	#**************************************************#

	def storeByTagsString(self, data_string, tags_string, delimiter = " "):
		if len(data_string) == 0:
			msg = {"status" : -1, "message" : "Data string is empty"}
			return json.dumps(msg)

		data_string, tag_list = Parser.parse_data_tags(data_string, tags_string, delimiter)

		if tag_list == None: 
			msg = {"status" : -2, "message" : "No tags in supplied data"}
			return json.dumps(msg)

		Datastore.UpdateTagValue(self.cur,data_string,tag_list)

	#**************************************************#

	def search(self, tags_list, searchtype="intersection"):

		if type(tags_list) is not list:
			return list(TagSearch.fetchByTag(tags_list))

		if searchtype == "intersection":
			return TagSearch.intersection(tags_list)

		elif searchtype == "union":
			return TagSearch.union(tags_list)

		elif searchtype == "symmetricDifference":
			return TagSearch.symmetricDifference(tags_list)

		else:
			return

	#**************************************************#

	def Delete(self, datasegment = None, tagslist = None):
		
		if datasegment is not None or tagslist is not None:
			if datasegment == None:
				Datastore.DeleteTag(self.cur,tagslist)
			elif tagslist == None:
				Datastore.DeleteValue(self.cur,datasegment)
			else:
				Datastore.DeleteValueByTags(self.cur,datasegment,tagslist)
		else:
			return -1

#**************************************************#

htags = hashTag("mysql","hashtags.db.10434227.hostedresource.com","hashtags","hashtags","code4Db@ba")

# htags.store("this is a post #selfie #facebook #twitter")

# storeByTags("H:/dev/python/web/a.py","#softwarepro")

# print htags.storeByTagsList("adivandhya",["  ","adi ",""])
# htags.Delete(tagslist = ["facebook","twitter"]);

# htags.Delete("1962")

# htags.Delete("1171",["mysql"])

#test cases for search

# print "mysql : " + str(htags.search("mysql"))
# print
# print "intersection : " + str(htags.search(["mysql","vbscript"],"intersection"))
# print
# print "union : " + str(htags.search(["mysql","vbscript"],"union"))
# print
# print "symmetricDifference : " + str(htags.search(["mysql","vbscript"],"symmetricDifference"))
