#####################################################################################################################
#											HASHTAG.py - HashTagging for dummies									#
#####################################################################################################################
#####################################################################################
#
# Query Repository
#
#####################################################################################

queryStore ={
				"mysql":{
							"databaseCreation":"CREATE DATABASE IF NOT EXISTS hash_tags",
							"tableCreation"   :"""
													CREATE TABLE IF NOT EXISTS table_name 
													 (
													  id AUTO_INCREMENT PRIMARY KEY,
													  download FLOAT,
													  testfield FLOAT 
													 ),
												""",
	

						},
				"sqlite3":{
							"databaseCreation":"",
							"tableCreation"   :"""
													CREATE TABLE IF NOT EXISTS table_name 
													 (
													  id AUTO_INCREMENT PRIMARY KEY,
													  download FLOAT,
													  testfield FLOAT 
													 ),
												""",
							
						},
				"postgresql":{
							"databaseCreation":"CREATE DATABASE IF NOT EXISTS hash_tags",
							"tableCreation"   :"""
													CREATE TABLE IF NOT EXISTS table_name 
													 (
													  id AUTO_INCREMENT PRIMARY KEY,
													  download FLOAT,
													  testfield FLOAT 
													 ),
												""",
							}
			}