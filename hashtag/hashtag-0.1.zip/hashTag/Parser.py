#####################################################################################################################
#											HASHTAG.py - HashTagging for dummies									#
#####################################################################################################################

from sets import Set
#***************************************#

def parse_data_tags(data_string, tags_string, delimeter):

	# data = userid
	# tags_string = "#tag1 #tag2 #tag3 #tag4"

	tags = tags_string.split(delimeter)

	tags = [tag.split("#")[1] for tag in tags]
	
	tags = [tag.strip() for tag in tags if len(tag.strip()) != 0]

	tags = list(Set(tags)) #isnt this operation of coverting to SET costly?

	return data, tags

#***************************************#

def parse_tags(data_tags_string):

	# data_tags_string = "Hello World #tag1 #tag2 #tag3 #tag4 Welcome Harish"

	tags = data_tags_string.split("#")

	data = data_tags_string

	tags = [tag.split(" ")[0] for tag in tags[1:]]

	tags = [tag.strip() for tag in tags if len(tag.strip()) != 0]
	
	tags = list(Set(tags))

	return data,tags

#***************************************#

# parse_tags("this is a post...#me #me #notme #adi #adi")