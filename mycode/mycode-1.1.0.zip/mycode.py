def repeatative_print (in_list, level):
	for each_item in in_list:
		if isinstance (each_item, list):
			repeatative_print (each_item)
		else:
			for tab_stop in range(level):
				print("\t", end='')
			print(each_item)