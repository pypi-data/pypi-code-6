"""This is a blabla."""
def print_lol(list1, indent = False, numOfTab = 0):
	for each_item in list1:
		if isinstance(each_item, list):
			print_lol(each_item, indent, numOfTab + 1)
		else:
			if indent is True:
				print ("\t" * numOfTab, end = '')
			print (each_item)





