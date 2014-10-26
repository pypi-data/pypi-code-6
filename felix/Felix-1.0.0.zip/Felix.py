import sys
def print_lol(the_list,indent = False,level = 0,out = sys.stdout):
	for each_item in the_list:
		if (isinstance(each_item, list)):
			print_lol(each_item,indent,level+1,out)
		else:
			if indent:
				for tab_stop in range(level):
					print('\t',end='',file = out)	# print函数自动包含换行功能，使用end = ''可以关闭此功能
			print(each_item,file = out)
