def print_lol(the_list,value=0):
	for each_item in the_list:
	 if isinstance(each_item, list):
	      print_lol(each_item,value+1)
	       
	 else:
	     for tab_stop in range (value):
	        print("\t",end='')
	print(each_item)
