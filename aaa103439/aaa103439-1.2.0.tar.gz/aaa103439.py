#模块名：aaa103439
#模块版本:python 3.4.1
#模块作用:打印嵌套列表
#模块参数：
"""	the_list:接收一个列表变量
	indent:接收True或者False,是否开启嵌套缩进
	level:接收一个缩进级别，即每次嵌套前缩进几个\t
"""
def print_lol(the_list, indent=False, level=0):
    for item1 in the_list:
        if isinstance(item1, list):
            print_lol(item1, indent, level + 1)
        else:
            if indent:
#	        for num in range(level):
#		    print("\t", end='')
                print("\t" *level, end='')
            print(item1)
