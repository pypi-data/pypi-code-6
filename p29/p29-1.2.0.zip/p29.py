"""This is a blabla."""
def print_lol(list1, numOfTab = 0):
	for each_item in list1:
		if isinstance(each_item, list):
			print_lol(each_item, numOfTab + 1)
		else:
			for num in range(numOfTab):
				print ("\t", end = '')
			print (each_item)





