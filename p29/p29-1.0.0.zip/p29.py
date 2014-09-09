def print_lol(list1):
	for each_item in list1:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print (each_item)





