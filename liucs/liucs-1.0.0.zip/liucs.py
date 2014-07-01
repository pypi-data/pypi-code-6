"""这是模块的描述."""
def print_lol(the_list):
	"""这是函数的描述"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)