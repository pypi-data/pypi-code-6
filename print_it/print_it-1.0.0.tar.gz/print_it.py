Python 3.4.0 (default, Apr 11 2014, 13:05:11) 
[GCC 4.8.2] on linux
Type "copyright", "credits" or "license()" for more information.
>>> def print_it(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_it(each_item)
		else:
			print(each_item)

			
>>> """this is a eaxmple of print out every element in list"""
def print_it(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_it(each_item)
		else:
			print(each_item)
