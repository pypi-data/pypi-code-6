"""
	通过print_lol(列表)函数调用打印多重列表
	其中可能包含（也可能不包含）嵌套列表。
"""
def print_lol (the_list,deep):
	"""
		 这个函数取一个位置参数，名为"the list",这可以是任何python列表（也可以是包含嵌套列表的列表的列表）。
		 所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项各占一行。
	"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,deep+1)
		else:
			for num in range(deep):
				print("\t",end="")
			print(each_item)