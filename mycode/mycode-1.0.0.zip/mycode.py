def repeatative_print (in_list):
	for each_item in in_list:
		if isinstance (each_item, list):
			repeatative_print (each_item)
		else:
			print(each_item)
