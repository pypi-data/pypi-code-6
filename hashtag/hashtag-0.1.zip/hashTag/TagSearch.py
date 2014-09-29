#####################################################################################################################
#											HASHTAG.py - HashTagging for dummies									#
#####################################################################################################################

from sets import Set
import DataFetchEngine

#Fetch values for Each tag and return List of values
def fetchByTag(cur, tag):

	data = DataFetchEngine.dataFetchByTag(cur, tag)
	
	return data.split(",")

def intersection(cur,tags_list):
	mainSet = Set()
	#tags_list ===>> Li st of tags sent by user
	for tag in tags_list:
		tempSet = Set(fetchByTag(tag)) #function call to get List of Values of each Tag
		
		if len(mainSet) == 0:
			mainSet = tempSet
		else:
			mainSet = mainSet & tempSet
		
	return list(mainSet)


def union(cur,tags_list):
	mainSet = Set()
	#tags_list ===>> List of tags sent by user
	for tag in tags_list:
		tempSet = Set(fetchByTag(tag)) #function call to get List of Values of each Tag
		if len(mainSet) == 0:
			mainSet = tempSet
		else:
			mainSet = mainSet | tempSet
	return list(mainSet)

def symmetricDifference(cur,tags_list):
	mainSet = Set()
	#tags_list ===>> List of tags sent by user
	for tag in tags_list:
		tempSet = Set(fetchByTag(tag)) #function call to get List of Values of each Tag
		if len(mainSet) == 0:
			mainSet = tempSet
		else:
			mainSet = mainSet ^ tempSet
	return list(mainSet)

#### Biased Searching that takes 2 list parameters Ex:--- [#aamir  & #khan] - [#bollywood | #actor] ####
def searchBiasedDifference(cur,positive_tags_list, negetive_tags_list):
	#Taking Intersection of all Positive Items and Union of all Negetive Items and find biased DIfference
	positive_temp_set = Set(intersection(positive_tags_list))	
	negetive_temp_set = Set(union(negetive_tags_list))

	#finding biased diff of both 
	mainSet = positive_temp_set - negetive_temp_set

	return list(mainSet)



# ######### TEST CASES ########

# print intersection(["sameer","rahul","adi"])
# print union(["sameer","rahul","adi"])
# print searchBiasedDifference(["sameer","adi"], ["rahul","sample"])
# print symmetricDifference(["sameer","rahul","adi"])

# ######### TEST CASES ########

