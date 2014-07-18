"""This module will help pint items in list of list.
   Additionaly allowing nested items to be printed 
   with tab stops. 
"""

def print_lol(the_list,level=0):
	"""This is a recursive function
	which takes two arguments. First one is a list
	and second is number of tab stops"""	  
	for nested_item in the_list:
		if isinstance(nested_item,list):
			print_lol(nested_item,level+1)
		else:	
			for tab_stop in range(level):
				print("\t",end="")
			print(nested_item)
