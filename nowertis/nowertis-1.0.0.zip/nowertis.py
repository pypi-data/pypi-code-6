"""this is my module with my functions"""

def print_lol(the_list):
		"""First example function"""
		for each_item in the_list:
			if isinstance(each_item, list):
				print_lol(each_item)
			else:
				print(each_item)
						
def suma(x,y):
	return x+y