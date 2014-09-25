"""nester.py with tabCount"""
def print_item(the_list, tabCount=0):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_item(each_item, tabCount+1)
		else:
			for tab_stop in range(tabCount):
				print("\t",end='#')
			print(each_item)
