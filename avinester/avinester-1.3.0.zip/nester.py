"""nester.py with tabCount"""
def print_item(the_list, indent=False, tabCount=0):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_item(each_item, indent, tabCount+1)
		else:
                        if indent:
                                for tab_stop in range(tabCount):
                                        print("\t",end='#')
                        print(each_item)
