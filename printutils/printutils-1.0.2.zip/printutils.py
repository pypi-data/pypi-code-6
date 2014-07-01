"""
递归打印list对象，如果对象中的元素也是list，则会缩进打印该元素的子元素，以此类推
同时可以指定缩进字符串，如果不指定，则默认为一个不缩进
"""
def print_list(p_list, intent_char="", level=0):
	# 循环的开始
	for an_item in p_list:
		if isinstance(an_item, list): # 如果元素也是列表类型，则递归打印该元素的子元素
			print("<Sub list>")
			print_list(an_item, intent_char, level + 1)
		else:
			print(intent_char * level, an_item)